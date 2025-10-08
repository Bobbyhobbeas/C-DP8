from datapunt9.models import Task, Personnel, Weather, PlannedPause, AdminBlock, IncidentBlock
from datapunt9.planner import genereer_dagtakenlijst




def mk_tasks():
return [
Task(id=1, omschrijving="Hoge prio spec", duur=45, prioriteit="Hoog", beroepstype="Mechanisch Monteur", bevoegdheid="Senior", attractie="Twister", is_buitenwerk=True),
Task(id=2, omschrijving="Hoge prio", duur=120, prioriteit="Hoog", beroepstype="Mechanisch Monteur", bevoegdheid="Senior", is_buitenwerk=False),
Task(id=3, omschrijving="Lage prio", duur=60, prioriteit="Laag", beroepstype="Mechanisch Monteur", bevoegdheid="Medior", is_buitenwerk=True),
]




def test_planner_basics():
p = Personnel(
naam="Piet", werktijd=240, beroepstype="Mechanisch Monteur", bevoegdheid="Senior",
specialist_in_attracties=["Twister"], pauze_opsplitsen=False, leeftijd=45, verlaagde_fysieke_belasting=None
)
w = Weather(temperatuur=20, kans_op_regen=10)
dag = genereer_dagtakenlijst(p, mk_tasks(), w)


# bevat taken + pauze + admin
assert any(isinstance(i, PlannedPause) for i in dag)
assert any(isinstance(i, AdminBlock) for i in dag)
# geen overschrijding door break-logic
total = sum(getattr(i, "duur", 0) for i in dag if not isinstance(i, IncidentBlock))
assert total <= p.werktijd




def test_planner_hitte_extra_pauze():
p = Personnel(
naam="Piet", werktijd=240, beroepstype="Mechanisch Monteur", bevoegdheid="Senior",
specialist_in_attracties=[], pauze_opsplitsen=True, leeftijd=45, verlaagde_fysieke_belasting=None
)
w = Weather(temperatuur=31, kans_op_regen=0)
dag = genereer_dagtakenlijst(p, mk_tasks(), w)
# 15 min extra pauze aanwezig
assert sum(getattr(i, "duur", 0) for i in dag if isinstance(i, PlannedPause)) >= 45
