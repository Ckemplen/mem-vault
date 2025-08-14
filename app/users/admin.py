from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("token", "expires_at", "used", "link")
    readonly_fields = ("token", "link", "created_at", "used")
    fields = ("email", "expires_at", "token", "created_at", "used", "link")

    def link(self, obj):
        url = reverse("register", args=[obj.token])
        return format_html('<a href="{0}">{0}</a>', url)

    link.short_description = "Invite Link"
