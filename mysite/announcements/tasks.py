from __future__ import absolute_import, unicode_literals
from celery import task
from django.utils import timezone
from .models import Announcements, AnnouncementDeliveryStatus
from django.db import transaction


@task()
def check_scheduled_announcements():
    current_time = timezone.now()

    scheduled_announcement = Announcements.objects.filter(date_time_to_publish__lte=current_time, sent_at=None)\
        .prefetch_related('groups__user_set')

    updated_announcement_ids = []
    bulk_status_update = []
    for announcement in scheduled_announcement:
        group_list = announcement.groups.all()

        user_list = [user for group in group_list for user in group.user_set.all()]
        user_list = set(user_list)

        for u in user_list:
            print("{} {} {}".format(u, announcement.title, announcement.message))
            bulk_status_update.append(AnnouncementDeliveryStatus(announcement_id=announcement.id, user_id=u.id,
                                                                 status_last_update_time=current_time,
                                                                 status=AnnouncementDeliveryStatus.YET_TO_RECEIVE))
        updated_announcement_ids.append(announcement.id)
    with transaction.atomic():
        AnnouncementDeliveryStatus.objects.bulk_create(bulk_status_update)
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

    with transaction.atomic():
        Announcements.objects.filter(id__in=expired_announcement_id).update(has_expired=True)
        AnnouncementDeliveryStatus.objects.filter(announcement_id__in=expired_announcement_id,
                                                  status=AnnouncementDeliveryStatus.YET_TO_RECEIVE)\
            .update(status=AnnouncementDeliveryStatus.EXPIRED, status_last_update_time=current_time)
