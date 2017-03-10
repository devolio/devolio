from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    """User Skills: takes a user, a skill and a level"""

    LEVEL_CHOICES = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert')
        )

    user = models.ForeignKey(User)
    name = models.CharField("Skill name", max_length=100)
    level = models.CharField("What's your level?", choices=LEVEL_CHOICES, max_length=50)
