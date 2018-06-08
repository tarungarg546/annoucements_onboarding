from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.auth.models import Group

@python_2_unicode_compatible
class Announcements(models.Model):
    is_active = models.BooleanField(default=False, help_text='Marked when announcement is active')
    has_expired = models.BooleanField(default=False, help_text='Marked when announcement expires')
    title = models.CharField(max_length=32, help_text='This will be shown as the title of notification and announcement')
    message = models.CharField(max_length=200, help_text='The message you want to convey')
    date_time_to_publish = models.DateTimeField('datetime publish', help_text='Schedule date and time for announcement')
    date_time_expire = models.DateTimeField('datetime expire', help_text='Expiry date and time for announcement')

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.title

    def clean(self):
        if self.date_time_to_publish <= timezone.now():
            raise ValidationError("The date and time can't be in past")
        if self.date_time_expire <= timezone.now():
            raise ValidationError("The date and time can't be in past")