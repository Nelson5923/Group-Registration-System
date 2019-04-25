from django.db import models
import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# User Creation

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sid = models.CharField(max_length=10) # Customized Field

class Project(models.Model):
    project_name = models.CharField(max_length=40, primary_key = True)
    min_member = models.CharField(max_length=3)
    max_member = models.CharField(max_length=3)
    deadline = models.DateField(null=False)
    description = models.CharField(max_length=200)

class Group(models.Model):

    # ForeignKeyField accept a object

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=40, default="")
    description = models.CharField(max_length=200, default="")
    members = models.ManyToManyField(User, through='Membership')

    # Create composite key

    class Meta:
        unique_together = (('group_name', 'project'),)

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'group'),)

# Update Profile when User Update

@receiver(post_save, sender=User)
def updateProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
