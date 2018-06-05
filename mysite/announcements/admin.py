from django.contrib import admin
from .models import Announcements
from django.contrib.auth.models import User


class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'date_time_expire')
    change_form_template = "announcements/announcements_change_form.html"

    def response_change(self, request, obj):
        if "_send_announcement" in request.POST:
            user_list = request.POST.getlist('users')
            users = User.objects.all()

            for u in user_list:
                for user in users:
                    if int(u) == user.id:
                        print str(user) + ' ' + request.POST['title'] + ' ' + request.POST['message']

        return super(AnnouncementsAdmin, self).response_change(request, obj)   


admin.site.register(Announcements, AnnouncementsAdmin)
