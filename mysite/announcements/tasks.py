from __future__ import absolute_import, unicode_literals

from celery import task
from django.utils import timezone

from .models import Announcements


@task()
def check_scheduled_announcements():
    current_time = timezone.now()
    scheduled_announcement = Announcements.objects.filter(date_time_to_publish__lte=current_time, sent_at=None)\
        .prefetch_related('groups__user_set')

    updated_announcement_ids = []
    for announcement in scheduled_announcement:
        group_list = announcement.groups.all()

        user_list = [user for group in group_list for user in group.user_set.all()]

        user_list = set(user_list)

        for u in user_list:
            print("{} {} {}".format(u, announcement.title, announcement.message))
            updated_announcement_ids.append(announcement.id)

    Announcements.objects.filter(id__in=updated_announcement_ids).update(sent_at=current_time)
