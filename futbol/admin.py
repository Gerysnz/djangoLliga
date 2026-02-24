from django.contrib import admin

from .models import Lliga, Equip, Jugador, Partit, Event

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)

class EventInline(admin.StackedInline):
    model = Event
    extra = 1

class PartitAdmin(admin.ModelAdmin):
    inlines = [EventInline]

admin.site.register(Partit, PartitAdmin)
