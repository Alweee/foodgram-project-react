from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Subscription, User


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'is_staff')
    list_filter = ('email', 'first_name',
                   'is_staff', 'is_superuser', 'is_active')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'author')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
