from django.contrib import admin

from django.contrib.admin.models import LogEntry

from app.models import Lab, Role, Request, LabCode, Notify, Subscription

class LabAdmin(admin.ModelAdmin):
    list_display=('lid','name', 'description', 'active')

class RoleAdmin(admin.ModelAdmin):
    list_display=('id', 'lid', 'uid', 'role')

class RequestAdmin(admin.ModelAdmin):
    list_display=('rid','station','description','timeSubmitted',
                  'timeCompleted','feedback','suid','lid','huid','complete')

class LabCodeAdmin(admin.ModelAdmin):
    list_display=('code','lid','role')

class NotifyAdmin(admin.ModelAdmin):
    list_display=('id', 'uid','lid','notifyNew','notifyThreshold')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display=('id', 'uid','initialSub', 'lastSub', 'subRenewal','labLimit', 'orderID')

class LogEntryAdmin(admin.ModelAdmin):
    list_display=("object_id", "content_type","action_flag","user","action_time")


admin.site.register(Lab, LabAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(LabCode, LabCodeAdmin)
admin.site.register(Notify, NotifyAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(LogEntry, LogEntryAdmin)

adminSite = admin.AdminSite

adminSite.site_header = "LabLineup Admin"
adminSite.site_title = "LabLineup Admin"
adminSite.index_title = "LabLineup Admin"