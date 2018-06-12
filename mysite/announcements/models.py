from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Announcements(models.Model):

    title = models.CharField(max_length=32, help_text='This will be shown as the title of notification and announcement')

    message = models.CharField(max_length=200, help_text='The message you want to convey')

    date_time_to_publish = models.DateTimeField('datetime publish', help_text='Schedule date and time for announcement')
    date_time_expire = models.DateTimeField('datetime expire', help_text='Expiry date and time for announcement')

    groups = models.ManyToManyField(Group)

    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField(editable=False)

    sent_at = models.DateTimeField(editable=False, null=True, blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        if (self.date_time_to_publish <= timezone.now()) or (self.date_time_expire <= timezone.now()):
            raise ValidationError("The date and time can't be in past")

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Announcements, self).save(*args, **kwargs)