from django.contrib import admin
from .models import Announcements

class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'date_time_expire')
    # list_display_links = ('title', 'message')


admin.site.register(Announcements, AnnouncementsAdmin)