from __future__ import absolute_import, unicode_literals

from celery import task
from django.utils import timezone

from .models import Announcements, Status


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
            Status.objects.create(announcement_id=announcement.id, user_id=u.id,
                                  status_last_update_time=current_time, status='yet to receive')

        updated_announcement_ids.append(announcement.id)

    Announcements.objects.filter(id__in=updated_announcement_ids).update(sent_at=current_time)


@task()
def expire_announcements():
    current_time = timezone.now()

    expired_announcements = Announcements.objects.exclude(sent_at=None)\
        .filter(has_expired=False, date_time_expire__lte=current_time)
    expired_announcement_id = []

    for announcement in expired_announcements:
        print ("{} {} has expired!".format(announcement.title, announcement.message))
        expired_announcement_id.append(announcement.id)

    Announcements.objects.filter(id__in=expired_announcement_id).update(has_expired=True)
    Status.objects.filter(announcement_id__in=expired_announcement_id, status='yet to receive')\
        .update(status='expired', status_last_update_time=current_time)
