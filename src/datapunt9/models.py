from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Fields


Priority = Literal["Hoog", "Laag"]
Seniority = Literal["Senior", "Medior", "Junior", "Stagiair"]
Beroep = Literal["Schilder", "Mechanisch Monteur", "Elektrisch Monteur", "Onderhoudsmonteur"]


class Personnel(BaseModel):
naam: str
werktijd: int # in minuten
beroepstype: Beroep
bevoegdheid: Seniority
specialist_in_attracties: List[str] = Field(default_factory=list)
pauze_opsplitsen: bool = False
leeftijd: int
verlaagde_fysieke_belasting: Optional[int] = None


class Task(BaseModel):
id: int
omschrijving: str
duur: int # minuten
prioriteit: Priority
beroepstype: Beroep
bevoegdheid: Seniority
fysieke_belasting: Optional[int] = None
attractie: Optional[str] = None
is_buitenwerk: bool = False


class Weather(BaseModel):
temperatuur: Optional[int] = None # °C
kans_op_regen: Optional[int] = None # %


class PlannedPause(BaseModel):
omschrijving: Literal["Pauze"] = "Pauze"
duur: int


class AdminBlock(BaseModel):
omschrijving: Literal["Administratietijd"] = "Administratietijd"
aantal_taken: int
duur: int


class IncidentBlock(BaseModel):
type: Literal["storingen"] = "storingen"
alternatieve_onderhoudstaken: List[Task]


DagItem = Task | PlannedPause | AdminBlock | IncidentBlock


class OutputModel(BaseModel):
personeelsgegevens: dict
weergegevens: dict
dagtaken: List[DagItem]
totale_duur: int
