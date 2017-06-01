from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class InlineProfile(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomAdmin(UserAdmin):
    inlines = (InlineProfile,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomAdmin)
