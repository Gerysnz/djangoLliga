from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import datetime
from random import randint

from futbol.models import Lliga, Equip, Jugador, Partit, Event

faker = Faker(["es_CA", "es_ES"])

class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'

    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)

    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        if Lliga.objects.filter(nom=titol_lliga).exists():
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return

        print(f"Creem la nova lliga: {titol_lliga}")
        lliga = Lliga(nom=titol_lliga, temporada="temporada", pais="Espanya")
        lliga.save()

        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        equips = []
        noms_usats = set()

        for i in range(20):
            intentos = 0
            while True:
                ciutat = faker.city()
                prefix = prefixos[randint(0, len(prefixos) - 1)]
                if prefix:
                    prefix += " "
                nom_equip = prefix + ciutat
                if nom_equip not in noms_usats:
                    noms_usats.add(nom_equip)
                    break
                intentos += 1
                if intentos > 50:
                    nom_equip = f"{nom_equip}_{i}"
                    noms_usats.add(nom_equip)
                    break

            equip = Equip(ciutat=ciutat, nom=nom_equip, lliga=lliga)
            equip.save()
            equips.append(equip)

            print(f"Creem jugadors de l'equip {nom_equip}")
            for j in range(25):
                jugador = Jugador(
                    nom=faker.first_name(),
                    cognoms=faker.last_name(),
                    dorsal=randint(1, 99),
                    edat=randint(18, 35),
                    equip=equip
                )
                jugador.save()

        print("Creem partits de la lliga")
        partits = []
        for local in equips:
            for visitant in equips:
                if local != visitant:
                    mes = randint(1, 12)
                    dia = randint(1, 28)
                    data_naive = datetime(2026, mes, dia)
                    data_aware = timezone.make_aware(data_naive)
                   



                    partit = Partit(
                        equip_local=local,
                        equip_visitant=visitant,
                        data=data_aware
                    )
                    partit.save()
                    partits.append(partit)

        for partit in partits:
            gols_local = randint(0, 5)
            gols_visitant = randint(0, 5)

            # Goles del equipo local
            for _ in range(gols_local):
                jugador = partit.equip_local.jugadors.order_by('?').first()
                minut = randint(0, 59)
                temps = timezone.now().replace(hour=0, minute=minut, second=0, microsecond=0).time()
                Event.objects.create(
                    partit=partit,
                    temps=temps,
                    tipus=Event.EventType.GOL,
                    jugador=jugador,
                    equip=partit.equip_local
                )

            # Goles del equipo visitante
            for _ in range(gols_visitant):
                jugador = partit.equip_visitant.jugadors.order_by('?').first()
                minut = randint(0, 59)
                temps = timezone.now().replace(hour=0, minute=minut, second=0, microsecond=0).time()
                Event.objects.create(
                    partit=partit,
                    temps=temps,
                    tipus=Event.EventType.GOL,
                    jugador=jugador,
                    equip=partit.equip_visitant
                )


        print(f"Lliga '{titol_lliga}' creada correctament amb {len(equips)} equips i jugadors.")