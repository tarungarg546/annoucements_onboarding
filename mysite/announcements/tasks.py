from __future__ import absolute_import, unicode_literals

from celery import task
from django.utils import timezone

from .models import Announcements


@task()
def check_scheduled_announcements():
    scheduled_announcement = Announcements.objects.filter(date_time_to_publish__lte=timezone.now())\
        .filter(sent_at=None)\
        .prefetch_related('groups__user_set')
    scheduled_announcement.update(sent_at=timezone.now())

    for announcement in scheduled_announcement:
        group_list = announcement.groups.all()
        user_list = []

        for group in group_list:
            users = group.user_set.all()
            for u in users:
                user_list.append(u)

        user_list = list(set(user_list))

        for u in user_list:
            print("{} {} {}".format(u, announcement.title, announcement.message))
