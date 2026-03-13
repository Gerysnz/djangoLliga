from django.db import models


class Lliga(models.Model):
    nom = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    temporada = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nom} ({self.temporada})"


class Equip(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    ciutat = models.CharField(max_length=100)

    lliga = models.ForeignKey(
        Lliga,
        on_delete=models.CASCADE,
        related_name="equips"
    )

    def __str__(self):
        return self.nom


class Jugador(models.Model):
    nom = models.CharField(max_length=100)

    equip = models.ForeignKey(
        Equip,
        on_delete=models.CASCADE,
        related_name="jugadors"
    )

    def __str__(self):
        return self.nom

    @property
    def gols(self):
        return (
            self.events_fets.filter(tipus=Event.EventType.GOL).count() +
            self.events_rebuts.filter(tipus=Event.EventType.AUTOGOL).count()
        )


class Partit(models.Model):

    equip_local = models.ForeignKey(
        Equip,
        on_delete=models.CASCADE,
        related_name="partits_local"
    )

    equip_visitant = models.ForeignKey(
        Equip,
        on_delete=models.CASCADE,
        related_name="partits_visitant"
    )

    data = models.DateTimeField()

    class Meta:
        unique_together = ("equip_local", "equip_visitant", "data")

    def __str__(self):
        return f"{self.equip_local} vs {self.equip_visitant} ({self.data.date()})"

    @property
    def lliga(self):
        return self.equip_local.lliga

    @property
    def gols_local(self):
        return (
            self.event_set.filter(
                tipus=Event.EventType.GOL,
                equip=self.equip_local
            ).count()
            +
            self.event_set.filter(
                tipus=Event.EventType.AUTOGOL,
                equip=self.equip_visitant
            ).count()
        )

    @property
    def gols_visitant(self):
        return (
            self.event_set.filter(
                tipus=Event.EventType.GOL,
                equip=self.equip_visitant
            ).count()
            +
            self.event_set.filter(
                tipus=Event.EventType.AUTOGOL,
                equip=self.equip_local
            ).count()
        )


class Event(models.Model):

    class EventType(models.TextChoices):
        GOL = "GOL"
        AUTOGOL = "AUTOGOL"
        FALTA = "FALTA"
        PENALTY = "PENALTY"
        MANS = "MANS"
        CESSIO = "CESSIO"
        FORA_DE_JOC = "FORA_DE_JOC"
        ASSISTENCIA = "ASSISTENCIA"
        TARGETA_GROGA = "TARGETA_GROGA"
        TARGETA_VERMELLA = "TARGETA_VERMELLA"

    partit = models.ForeignKey(
        Partit,
        on_delete=models.CASCADE
    )

    temps = models.TimeField()

    tipus = models.CharField(
        max_length=30,
        choices=EventType.choices
    )

    jugador = models.ForeignKey(
        Jugador,
        null=True,
        on_delete=models.SET_NULL,
        related_name="events_fets"
    )

    equip = models.ForeignKey(
        Equip,
        null=True,
        on_delete=models.SET_NULL
    )

    jugador2 = models.ForeignKey(
        Jugador,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="events_rebuts"
    )

    detalls = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipus_display()} de {self.jugador} al minut {self.temps.minute} del partit {self.partit}"