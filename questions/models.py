from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver

from taggit.managers import TaggableManager
import mistune

from slackclient import SlackClient

from utils.slugger import unique_slugify

from devolio.settings import SLACK_TOKEN, BASE_URL

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

    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True,
                                      editable=False, verbose_name='Date added')
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True,
                                         verbose_name='Last modified')

    def save(self, *args, **kwargs):
        self.body_html = mistune.markdown(self.body_md)
        super(Response, self).save(*args, **kwargs)

    def __str__(self):
        return "Response to {}".format(self.question)


def slack_msg(instance):
    return {
        "title": instance.title,
        "author_name": "@{}".format(instance.user.username),
        "author_link": "{}/@{}".format(BASE_URL, instance.user.username),
        "color": "#f78250",
        "title_link": "{}{}".format(BASE_URL, instance.get_absolute_url()),
        "pretext": "New question!",
        "footer": "devolio.net",
        }


@receiver(post_save, sender=Question)
def post2slack(sender, instance, **kwargs):
    if SLACK_TOKEN:
        sc = SlackClient(SLACK_TOKEN)
        sc.api_call(
        "chat.postMessage",
        channel="#devolio_questions",
        attachments=[slack_msg(instance)]
        )
