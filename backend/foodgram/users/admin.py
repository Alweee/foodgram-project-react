from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Subscription


class CustomUserAdmin(UserAdmin):
    list_filter = ('email', 'first_name',
                   'is_staff', 'is_superuser', 'is_active')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'author')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
