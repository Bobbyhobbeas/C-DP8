from __future__ import annotations
from typing import Iterable, List
from .models import Personnel, Task, Weather


# ---------- FR4 (maximale fysieke belasting) helper ----------


def bereken_max_belasting(leeftijd: int, verlaagde: int | None) -> int:
if verlaagde is not None:
return max(0, int(verlaagde))
if leeftijd <= 24:
return 25
if 25 <= leeftijd <= 50:
return 40
return 20 # 51+


# ---------- Filtering op profiel (FR6) ----------


def filter_op_profiel(taken: Iterable[Task], p: Personnel) -> List[Task]:
return [t for t in taken if t.beroepstype == p.beroepstype and _bevoegdheid_ok(p, t)]


def _bevoegdheid_ok(p: Personnel, t: Task) -> bool:
levels = ["Stagiair", "Junior", "Medior", "Senior"]
return levels.index(p.bevoegdheid) >= levels.index(t.bevoegdheid)


# ---------- Fysieke belasting (FR4) ----------


def filter_op_belasting(taken: Iterable[Task], maxkg: int) -> List[Task]:
res: List[Task] = []
for t in taken:
if t.fysieke_belasting is None or t.fysieke_belasting <= maxkg:
res.append(t)
return res


# ---------- Regenfilter voor schilders (FR15) ----------


def filter_op_buitenwerk_als_regen(taken: Iterable[Task], p: Personnel, regen_pct: int | None) -> List[Task]:
if p.beroepstype != "Schilder" or regen_pct is None or regen_pct < 50:
return list(taken)
return [t for t in taken if not t.is_buitenwerk]


# ---------- Sortering: prioriteit & specialisme (FR8) ----------


def sorteer_prioriteit_en_specialisme(taken: Iterable[Task], p: Personnel) -> List[Task]:
def key(t: Task):
prio_score = 0 if t.prioriteit == "Hoog" else 1
spec_score = 0 if (t.attractie and t.attractie in p.specialist_in_attracties) else 1
return (prio_score, spec_score, -t.duur) # langere taken eerst bij gelijke ranking
return sorted(taken, key=key)


# ---------- FR7: lagere bevoegdheidstaken oppakken als tijd over is ----------


def vul_met_lagere_bevoegdheid(origineel: Iterable[Task], alle_taken: Iterable[Task], p: Personnel) -> List[Task]:
selected_ids = {t.id for t in origineel}
levels = ["Stagiair", "Junior", "Medior", "Senior"]
p_level = levels.index(p.bevoegdheid)
# Neem alleen taken met lager level (en passend beroepstype)
candidates = [
t for t in alle_taken
if t.id not in selected_ids and t.beroepstype == p.beroepstype and levels.index(t.bevoegdheid) <= p_level
]
return list(origineel) + candidates
