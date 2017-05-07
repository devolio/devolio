import re

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail

from taggit.managers import TaggableManager
import mistune
from slackclient import SlackClient

from utils.slugger import unique_slugify
from django.conf import settings


class Question(models.Model):
    user = models.ForeignKey(User)

    title = models.CharField('Question title', max_length=50, blank=False)
    body_md = models.TextField('Question body (Markdown)', blank=True)
    body_html = models.TextField(blank=True)

    tags = TaggableManager(blank=False)

    slug = models.SlugField()

    points = models.ManyToManyField(User, blank=True, related_name='q_points')
    points_calc = models.IntegerField(default=0)

    pre_answered = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('q_detail', args=(self.slug,))

    def save(self, *args, **kwargs):
        self.body_html = mistune.markdown(self.body_md)
        if not self.slug:
            unique_slugify(self, self.title)
        super(Question, self).save(*args, **kwargs)


class Response(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)

    body_md = models.TextField('Response body (Markdown)', blank=True)
    body_html = models.TextField(blank=True)

    spam = models.BooleanField(default=False)
    answer = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,
        editable=False, verbose_name='Date added')
    updated = models.DateTimeField(
        auto_now=True, null=True, blank=True,
        verbose_name='Last modified')

    def save(self, *args, **kwargs):
        self.body_html = mistune.markdown(self.body_md)
        super(Response, self).save(*args, **kwargs)

    def __str__(self):
        return "Response to {}".format(self.question)

    @property
    def likes(self):
        return self.responsereaction_set.all().count()


class ResponseReaction(models.Model):
    user = models.ForeignKey(User)
    response = models.ForeignKey(Response)
    kind = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True, null=True,
                                      blank=True, editable=False,
                                      verbose_name='Date added')
    last_modified = models.DateTimeField(auto_now=True, null=True,
                                         blank=True,
                                         verbose_name='Last modified')

    def __unicode__(self):
        return f"{self.user} likes {self.response}"


def full_url(path):
    return "{}{}".format(settings.BASE_URL, path)


def slack_msg(instance):
    return {
        "title": instance.title,
        "author_name": "@{}".format(instance.user.username),
        "author_link": "{}/@{}".format(settings.BASE_URL, instance.user.username),
        "color": "#f78250",
        "title_link": full_url(instance.get_absolute_url()),
        "pretext": "New question!",
        "footer": "devolio.net",
        }


@receiver(post_save, sender=Question)
def post2slack(sender, instance, created, **kwargs):
    """
    Sends every new question to the #devolio_questions channel on Slack.
    """
    if not created or not settings.SLACK_TOKEN or settings.OFFLINE_DEV:
        return

    sc = SlackClient(settings.SLACK_TOKEN)
    sc.api_call(
        "chat.postMessage",
        channel="#devolio_questions",
        attachments=[slack_msg(instance)]
        )


REPLY_EMAIL = """
Hi {},\n
{} just left an answer on your question: {}\n
View it here: {}
\n
Have a nice day!
"""


@receiver(post_save, sender=Response)
def new_response_email(sender, instance, created, **kwargs):
    """
    Sends an email of new responses to the question author.
    instance == Response instance
    """
    if settings.OFFLINE_DEV or not created:
        return

    email = instance.question.user.email
    ques = instance.question
    resp_count = ques.response_set.count()

    # Send the question author a response notification if the they have
    # an email address and the question has less than 3 responses then.
    if email and resp_count < 3 and instance.user != ques.user:
        send_mail(
            subject='New response for {}'.format(ques.title),
            message=REPLY_EMAIL.format(
                ques.user,
                instance.user,
                ques.title,
                full_url(ques.get_absolute_url())
                ),
            from_email='hello@devolio.net',
            recipient_list=[email],
            fail_silently=True,
            )


MENTION_EMAIL = """
Hi {},\n
{} just mentioned you on this question: {}\n
View it here: {}
\n
Have a nice day!
"""


@receiver(post_save, sender=Response)
def notify_mention(sender, instance, created, **kwargs):
    if not created:
        # If this was only an update (!created), then do nothing
        return

    ques = instance.question

    # get all @mentions. TODO: This needs to be optimized by excluding @strings
    # in <code> and <pre> tags
    mentions = re.findall('\B@[a-z0-9_-]+', instance.body_md)
    for mention in mentions:
        username = mention.replace('@', '')
        try:
            user = User.objects.get(username=username)
            if user == instance.user or not user.email:
                # if a user mentions themselves or they don't have an email,
                # then do nothing
                return

            # Send an email to the user
            send_mail(
                subject='Somebody mentioned you on Devolio',
                message=MENTION_EMAIL.format(
                    user,
                    instance.user,
                    ques.title,
                    full_url(ques.get_absolute_url())
                    ),
                from_email='hello@devolio.net',
                recipient_list=[user.email],
                fail_silently=True,
                )

        except User.DoesNotExist:
            # Could not find a user with this username
            pass
