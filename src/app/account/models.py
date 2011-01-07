# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import UserManager, User as AuthUser
from django.db.models.signals import post_save 

class UserGroup(models.Model):
    name = models.CharField(u'Название', max_length=255)

    class Meta:
        verbose_name = u'групу'
        verbose_name_plural = u'групы'
    
    def __unicode__(self):
        return self.name

class User(AuthUser):
    group = models.ForeignKey(UserGroup, verbose_name=u'Група', null=True, blank=True)
    
    objects = UserManager()
    
    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return
    values = {}
    for field in sender._meta.local_fields:
        values[field.attname] = getattr(instance, field.attname)
    user = User(**values)
    user.save()

post_save.connect(create_user_profile, sender=AuthUser)