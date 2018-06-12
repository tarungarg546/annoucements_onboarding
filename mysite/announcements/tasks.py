from __future__ import absolute_import, unicode_literals

from celery import task
from django.utils import timezone

from .models import Announcements


@task()
def check_scheduled_announcements():
    current_time = timezone.now()
    scheduled_announcement = Announcements.objects.filter(date_time_to_publish__lte=current_time)\
        .filter(sent_at=None)\
        .prefetch_related('groups__user_set')

    announcement_id = []
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
        announcement_id.append(announcement.id)

    Announcements.objects.filter(id__in=announcement_id).update(sent_at=current_time)
