from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "phone_number", "created_at", "updated_at")
    search_fields = ("user__email", "location", "phone_number")
    ordering = ("-created_at",)


admin.site.register(Profile, ProfileAdmin)
