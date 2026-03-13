from django.shortcuts import render
from .models import Lliga

def classificacio(request):
    lliga = Lliga.objects.first()
    equips = lliga.equips.all()
    classi = []
 
    # calculem punts
    for equip in equips.all():
        punts = 0

        #equipos locales
        for partit in equip.partits_local.all():
            if partit.gols_local > partit.gols_visitant:
                punts += 3
            elif partit.gols_local == partit.gols_visitant:
                punts += 1

        #equipos visitantes
        for partit in equip.partits_visitant.all():
            if partit.gols_local < partit.gols_visitant:
                punts += 3
            elif partit.gols_local == partit.gols_visitant:
                punts += 1
        classi.append((punts, equip.nom))


    classi.sort(reverse=True)

    return render(request, "classificacio.html", {
        "classificacio": classi,
    })