from django.db import models

from taggit.models import TagBase, GenericTaggedItemBase


class SkillTag(TagBase):

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class GoodSkillTag(GenericTaggedItemBase):
    tag = models.ForeignKey(SkillTag, related_name="good_skill_tag")


class LearningSkillTag(GenericTaggedItemBase):
    tag = models.ForeignKey(SkillTag, related_name="learning_skill_tag")