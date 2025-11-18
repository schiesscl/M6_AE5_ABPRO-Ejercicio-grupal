from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'location', 'is_private', 'organizer']
    list_filter = ['event_type', 'is_private', 'date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date'
    filter_horizontal = ['attendees']
