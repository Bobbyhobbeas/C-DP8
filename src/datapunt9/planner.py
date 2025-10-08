from __future__ import annotations
from typing import List, Iterable
from .models import Personnel, Task, Weather, PlannedPause, AdminBlock, IncidentBlock, DagItem
from .rules import (
bereken_max_belasting,
filter_op_profiel,
filter_op_belasting,
filter_op_buitenwerk_als_regen,
sorteer_prioriteit_en_specialisme,
vul_met_lagere_bevoegdheid,
)


# Kern-algoritme: implementeert FR5, FR8, FR9, FR11, FR14 (+ optioneel FR7, FR10, FR12, FR13, FR15, FR16)


def genereer_dagtakenlijst(p: Personnel, alle_taken: Iterable[Task], weather: Weather) -> List[DagItem]:
rest = p.werktijd
dag: List[DagItem] = []


# FR16: Extra pauze bij hitte (>30°C)
if weather.temperatuur is not None and weather.temperatuur > 30:
dag.append(PlannedPause(duur=15))
rest -= 15


# Max. fysieke belasting
maxkg = bereken_max_belasting(p.leeftijd, p.verlaagde_fysieke_belasting)


# Filter op profiel (FR6) en belasting (FR4)
geschikt = filter_op_profiel(alle_taken, p)
geschikt = filter_op_belasting(geschikt, maxkg)


# FR15: Bij regen en schilder: alleen binnenwerk
geschikt = filter_op_buitenwerk_als_regen(geschikt, p, weather.kans_op_regen)


# Sorteer op prioriteit + specialisme (FR8)
geschikt = sorteer_prioriteit_en_specialisme(geschikt, p)


toegewezen: List[Task] = []
elapsed = 0
tijd_voor_storingsblok = 120 # elke ~2 uur


# Allocatie-loop tot werktijd bereikt (FR5 + FR9)
for taak in geschikt:
# FR13: Voeg storingsblok (1h) in voor seniors ongeveer elke 2h
if p.bevoegdheid == "Senior" and elapsed >= tijd_voor_storingsblok:
storings_alternatieven = [t for t in geschikt if t.prioriteit == "Laag"][:2]
dag.append(IncidentBlock(alternatieve_onderhoudstaken=storings_alternatieven))
elapsed = 0 # reset teller binnen blokken


if taak.duur <= rest:
toegewezen.append(taak)
rest -= taak.duur
elapsed += taak.duur
else:
break # FR9: stop wanneer volgende taak niet past


# FR7: Vul optioneel aan met lagere bevoegdheidstaken (indien nog resttijd)
if rest > 0:
aangevuld = sorteer_prioriteit_en_specialisme(vul_met_lagere_bevoegdheid(toegewezen, alle_taken, p), p)
for taak in aangevuld:
if taak in toegewezen:
continue
if taak.duur <= rest:
toegewezen.append(taak)
rest -= taak.duur
else:
break


# Voeg toegewezen taken toe aan daglijst
dag.extend(toegewezen)


# FR11: Pauze toevoegen (30 min). Opsplitsen per flag (FR12)
pauze_duur = 30
if p.pauze_opsplitsen:
dag.append(PlannedPause(duur=15))
dag.append(PlannedPause(duur=15))
rest -= pauze_duur
else:
dag.append(PlannedPause(duur=pauze_duur))
rest -= pauze_duur


# FR10: Administratietijd 2 min per taak
aantal_onderhoud = sum(1 for i in dag if not isinstance(i, (PlannedPause, AdminBlock, IncidentBlock)))
admin_duur = max(0, aantal_onderhoud * 2)
# Laat admin niet werktijd overschrijden
if admin_duur > rest:
admin_duur = max(0, rest)
dag.append(AdminBlock(aantal_taken=aantal_onderhoud, duur=admin_duur))


return dag
