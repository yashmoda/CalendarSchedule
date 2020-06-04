from django.contrib import admin
from calendar_schedule.models import UserData, CalendarData


class UserDataAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email_id']
    list_display = ['name', 'email_id', 'password']


admin.site.register(UserData, UserDataAdmin)


class CalendarDataAdmin(admin.ModelAdmin):
    search_fields = ['user_id', 'user_id', 'event_name', 'event_date', 'event_time']
    list_display = ['user_id', 'user_id', 'event_name', 'event_date', 'event_time']


admin.site.register(CalendarData, CalendarDataAdmin)
