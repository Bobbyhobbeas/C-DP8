from __future__ import annotations
from typing import List, Dict, Any
from .models import Personnel, Weather, Task, PlannedPause, AdminBlock, IncidentBlock, OutputModel, DagItem




def to_acceptance_json(
personnel: Personnel,
weather: Weather,
dagtaken: List[DagItem]
) -> Dict[str, Any]:
# Personeelsgegevens conform schema
pg = {
"Naam": personnel.naam,
"Werktijd": personnel.werktijd,
"Beroepstype": personnel.beroepstype,
"Bevoegdheid": personnel.bevoegdheid,
"Specialist_in_attracties": personnel.specialist_in_attracties,
"Pauze_opsplitsen": personnel.pauze_opsplitsen,
"Max_fysieke_belasting": None, # wordt in planner ingevuld
}


wg = {
"temperatuur": weather.temperatuur,
"kans_op_regen": weather.kans_op_regen,
}


lijst: List[dict] = []
totale = 0
for item in dagtaken:
if isinstance(item, Task):
obj = {
"omschrijving": item.omschrijving,
"duur": item.duur,
"prioriteit": item.prioriteit,
"beroepstype": item.beroepstype,
"bevoegdheid": item.bevoegdheid,
"fysieke_belasting": item.fysieke_belasting,
"attractie": item.attractie,
"is_buitenwerk": item.is_buitenwerk,
}
totale += item.duur
elif isinstance(item, PlannedPause):
obj = {"omschrijving": item.omschrijving, "duur": item.duur}
totale += item.duur
elif isinstance(item, AdminBlock):
obj = {
"omschrijving": item.omschrijving,
"aantal_taken": item.aantal_taken,
"duur": item.duur,
}
totale += item.duur
elif isinstance(item, IncidentBlock):
obj = {
"type": item.type,
"alternatieve_onderhoudstaken": [
{
"omschrijving": t.omschrijving,
"duur": t.duur,
"prioriteit": t.prioriteit,
"beroepstype": t.beroepstype,
"bevoegdheid": t.bevoegdheid,
"fysieke_belasting": t.fysieke_belasting,
"attractie": t.attractie,
"is_buitenwerk": t.is_buitenwerk,
}
for t in item.alternatieve_onderhoudstaken
],
}
else:
raise TypeError("Onbekend dagitem")
lijst.append(obj)


return OutputModel(
personeelsgegevens=pg,
weergegevens=wg,
dagtaken=lijst, # type: ignore
totale_duur=totale,
).model_dump()
