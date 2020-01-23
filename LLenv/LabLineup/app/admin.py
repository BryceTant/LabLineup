from django.contrib import admin

from app.models import Lab, Role, Request, LabCode, Notify, Subscription

class LabAdmin(admin.ModelAdmin):
    list_display=('lid','name', 'description')

class RoleAdmin(admin.ModelAdmin):
    list_display=('lid', 'uid', 'role')

class RequestAdmin(admin.ModelAdmin):
    list_display=('rid','station','description','timeSubmitted',
                  'timeCompleted','feedback','suid','lid','huid')

class LabCodeAdmin(admin.ModelAdmin):
    list_display=('code','lid','role')

class NotifyAdmin(admin.ModelAdmin):
    list_display=('uid','lid','notifyNew','notifyThreshold')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display=('uid','initialSub','subRenewal','labLimit')


admin.site.register(Lab, LabAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(LabCode, LabCodeAdmin)
admin.site.register(Notify, NotifyAdmin)
admin.site.register(Subscription, SubscriptionAdmin)