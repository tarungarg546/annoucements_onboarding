from __future__ import absolute_import, unicode_literals
from celery import task
from .models import Announcements
from django.utils import timezone
from django.contrib.auth.models import User, Group

@task()
def check_scheduled_announcements():
    scheduled_announcement = Announcements.objects.filter(is_active=False).filter(date_time_to_publish__lte=timezone.now())
    for announcement in scheduled_announcement:
        announcement.is_active = True
        announcement.save()
        group_list = announcement.groups.all().prefetch_related('id')
        group_users = User.objects.values_list('username', flat=True).filter(groups__id__in=group_list).distinct()

        for user in group_users:
            print("{} {} {}".format(user, announcement.title, announcement.message))
