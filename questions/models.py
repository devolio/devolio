from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
import mistune

from utils.slugger import unique_slugify


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

    def __unicode__(self):
        return self.user
