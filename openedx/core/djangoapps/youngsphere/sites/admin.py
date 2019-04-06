from django.contrib.auth.models import User
from ratelimitbackend import admin
from student.admin import UserAdmin
from .models import *


class AlternativeDomainAdmin(admin.ModelAdmin):
    list_display = (
        'domain',
        'site'
    )


admin.site.unregister(User)
#admin.site.register(AlternativeDomain, AlternativeDomainAdmin)
admin.site.register(User)
admin.site.register(UserMiniProfile)
admin.site.register(School)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(UserSectionMapping)

#socialwall admin integration
admin.site.register(Page)
admin.site.register(FeedModerator)
admin.site.register(GlobalGroup)
admin.site.register(SchoolGroup)
admin.site.register(Follow)
