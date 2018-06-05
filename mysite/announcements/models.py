import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

@python_2_unicode_compatible
class Announcements(models.Model):
    title = models.CharField(max_length=32, help_text='This will be shown as the title of notification and announcement')
    message = models.CharField(max_length=200, help_text='The message you want to convey')
    # date_time_published = models.DateTimeField('datetime published', help_text='The date and time you want to schedule announcement/notification')
    date_time_expire = models.DateTimeField('datetime expire', help_text='The date and time you want the announcement to expire')

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    users = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    def clean(self):
        # if self.date_time_published <= timezone.now():
        #     raise ValidationError("The date and time can't be in past")
        if self.date_time_expire <= timezone.now():
            raise ValidationError("The date and time can't be in past")