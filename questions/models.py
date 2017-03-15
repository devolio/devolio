from django.db import models
from django.contrib.auth.models import User

from utils.slugger import unique_slugify

from taggit.managers import TaggableManager
import mistune


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
        self.user = User.objects.get(pk=1)
        self.body_html = mistune.markdown(self.body_md)
        if not self.slug:
            unique_slugify(self, self.title)
        super(Question, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '/q/{}'.format(self.slug)
