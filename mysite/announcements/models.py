from django.contrib.auth.models import Group, User
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

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    sent_at = models.DateTimeField(editable=False, null=True, blank=True)

    has_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def clean(self):
        if (self.date_time_to_publish <= timezone.now()) or (self.date_time_expire <= timezone.now()):
            raise ValidationError("The date and time can't be in past")
        if self.date_time_expire <= self.date_time_to_publish:
            raise ValidationError("Scheduled time can't be less than expiry time")


@python_2_unicode_compatible
class AnnouncementDeliveryStatus(models.Model):
    SEEN = 0
    YET_TO_RECEIVE = 1
    EXPIRED = 2
    USER_LEFT_GROUP = 3

    STATUS_CHOICES = (
        (SEEN, 'SEEN'),
        (YET_TO_RECEIVE, 'YET TO RECEIVE'),
        (EXPIRED, 'EXPIRED'),
        (USER_LEFT_GROUP, 'USER LEFT GROUP')
    )
    announcement = models.ForeignKey(Announcements, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    status_last_update_time = models.DateTimeField('status last update time',
                                                   help_text='The time at status got updated')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return "{} {}".format(self.announcement, self.user)
