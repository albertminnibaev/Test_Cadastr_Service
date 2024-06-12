from django.contrib import admin

from server.models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'cadastral_number', 'latitude', 'longitude', 'server_response', 'created_at')
