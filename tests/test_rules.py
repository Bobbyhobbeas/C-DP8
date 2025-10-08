from datapunt9.models import Task, Personnel
from datapunt9.rules import (
bereken_max_belasting,
filter_op_profiel,
filter_op_belasting,
sorteer_prioriteit_en_specialisme,
)




def mk_p():
return Personnel(
naam="Piet", werktijd=480, beroepstype="Mechanisch Monteur", bevoegdheid="Senior",
specialist_in_attracties=["Twister"], pauze_opsplitsen=False, leeftijd=45, verlaagde_fysieke_belasting=None
)




def test_belasting_grenzen():
assert bereken_max_belasting(24, None) == 25
assert bereken_max_belasting(25, None) == 40
assert bereken_max_belasting(51, None) == 20
assert bereken_max_belasting(30, 30) == 30




def test_filter_profiel_en_belasting():
p = mk_p()
taken = [
Task(id=1, omschrijving="A", duur=30, prioriteit="Hoog", beroepstype="Mechanisch Monteur", bevoegdheid="Senior", fysieke_belasting=35, is_buitenwerk=True),
Task(id=2, omschrijving="B", duur=30, prioriteit="Laag", beroepstype="Schilder", bevoegdheid="Senior", fysieke_belasting=10, is_buitenwerk=False),
]
f = filter_op_profiel(taken, p)
assert len(f) == 1 and f[0].id == 1
f2 = filter_op_belasting(f, 30)
assert len(f2) == 0




def test_sort_prio_specialisme():
p = mk_p()
t1 = Task(id=1, omschrijving="X", duur=30, prioriteit="Hoog", beroepstype=p.beroepstype, bevoegdheid="Senior", attractie="Twister", is_buitenwerk=True)
t2 = Task(id=2, omschrijving="Y", duur=30, prioriteit="Hoog", beroepstype=p.beroepstype, bevoegdheid="Senior", attractie=None, is_buitenwerk=True)
t3 = Task(id=3, omschrijving="Z", duur=30, prioriteit="Laag", beroepstype=p.beroepstype, bevoegdheid="Senior", attractie=None, is_buitenwerk=True)
ordered = [t.id for t in sorteer_prioriteit_en_specialisme([t3, t2, t1], p)]
assert ordered == [1, 2, 3]
