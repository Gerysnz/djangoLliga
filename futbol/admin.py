from django.contrib import admin
from .models import Lliga, Equip, Jugador, Partit, Event


admin.site.register(Lliga)
admin.site.register(Equip)


class EventInline(admin.StackedInline):

    model = Event
    exclude = ('detalls',)
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # filtramos los jugadores para que solo aparezcan los de los 2 equipos del partido
        if db_field.name == "jugador":

            partit_id = request.resolver_match.kwargs.get("object_id")

            if partit_id:
                partit = Partit.objects.get(id=partit_id)

                jugadors_local = [j.id for j in partit.equip_local.jugadors.all()]
                jugadors_visitant = [j.id for j in partit.equip_visitant.jugadors.all()]

                jugadors = jugadors_local + jugadors_visitant

                kwargs["queryset"] = Jugador.objects.filter(id__in=jugadors)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PartitAdmin(admin.ModelAdmin):

    inlines = [EventInline]

    list_display = [
        "lliga",
        "equip_local",
        "equip_visitant",
        "data",
        "gols_local",
        "gols_visitant"
    ]

    search_fields = [
        "equip_local__nom",
        "equip_visitant__nom",
        "equip_local__lliga__nom"
    ]


class JugadorAdmin(admin.ModelAdmin):

    list_display = [
        "nom",
        "equip",
        "gols"
    ]

    search_fields = [
        "nom",
        "equip__nom"
    ]


admin.site.register(Partit, PartitAdmin)
admin.site.register(Jugador, JugadorAdmin)