from django.contrib import admin
from django.contrib.auth.models import User
from .models import Announcements


class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('title', 'message','date_time_to_publish', 'date_time_expire')
    change_form_template = "announcements/announcements_change_form.html"

    def response_change(self, request, obj):
        if "_send_announcement" in request.POST:
            group_list = request.POST.getlist('groups')
            group_users = User.objects.values_list('username', flat=True).filter(groups__id__in=group_list).distinct()

            for user in group_users:
                print("{} {} {}".format(str(user), request.POST['title'], request.POST['message']))

        return super(AnnouncementsAdmin, self).response_change(request, obj)   


admin.site.register(Announcements, AnnouncementsAdmin)
