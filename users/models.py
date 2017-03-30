from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager

from .tags import GoodSkillTag, LearningSkillTag
from utils.slugger import unique_slugify


def clean_url(url):
    return url.replace('https://', '').replace('http://', '')


class Profile(models.Model):
    user = models.OneToOneField(User, blank=False, unique=True)

    summary = models.TextField(max_length=256, blank=True)

    good_skills = TaggableManager("My Good Skills", through=GoodSkillTag,
            blank=True, related_name="user_good_skill")
    learning_skills = TaggableManager("Skills I'm still learning",
            through=LearningSkillTag,
            blank=True, related_name="user_learning_skill")


    slack_handle = models.CharField(blank=True, max_length=50)

    code_url = models.URLField('Code URL (eg. GitHub)', blank=True)
    website = models.URLField('Eg. Website, Twitter, portfolio', blank=True)

    

    slug = models.SlugField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def slack_url(self):
        if self.slack_handle:
            url = "https://devolio-devchat.slack.com/messages/@{}/"
            return url.format(self.slack_handle)

    @property
    def code_clean(self):
        return clean_url(self.code_url)

    @property
    def website_clean(self):
        return clean_url(self.website)

    def get_absolute_url(self):
        return reverse('public_profile', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
