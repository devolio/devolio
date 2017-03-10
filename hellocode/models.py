from django.contrib.auth.models import User
from django.db import models

from users.models import Skill


class CoderProfile(models.Model):
    """A model to store a 'Hello Coders' details"""
    user = models.OneToOneField(User)
    email = models.EmailField(blank=True)


class  ContribSkill(models.Model):
    """A skills, the user can contribute to OS with"""
    user = models.ForeignKey(User)
    skill = models.ForeignKey(Skill)
