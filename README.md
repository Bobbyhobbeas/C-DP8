# DP9 – Codekwaliteit

Generatie van een **dagtakenlijst** voor een personeelslid op basis van:
- beschikbare onderhoudstaken,
- personeelsprofiel (beroep/bevoegdheid/specialismes),
- **weergegevens** (temperatuur + regen) via een API.

Output is een **acceptatie-JSON** volgens het gevraagde format (personeelsgegevens, weergegevens, dagtaken, totale duur).

## Inhoud
- [Features / FR-overzicht](#features--fr-overzicht)
- [Architectuur](#architectuur)
- [Installatie](#installatie)
- [Gebruik](#gebruik)
- [Configuratie](#configuratie)
- [Voorbeeldoutput](#voorbeeldoutput)
- [Testen](#testen)
- [Kwaliteit (rubric)](#kwaliteit-rubric)
- [Git-werkwijze](#git-werkwijze)

---

## Features / FR-overzicht

| FR | Omschrijving | Implementatie |
|---|---|---|
| FR5 | Werktijd niet overschrijden | Planner breekt zodra volgende taak niet past |
| FR8 | Prioriteit + specialisme vóórrang | Sorteerfunctie op prio en attractie-specialisme |
| FR9 | Stoppen wanneer volgende taak niet past | Break-logic in allocatieloop |
| FR11 | Pauze | 30 min; opsplitsbaar (FR12) |
| FR14 | Weer-API (temperatuur) | Open-Meteo client + fallback |
| FR7 | Lagere bevoegdheid bij resttijd | Optionele aanvulling |
| FR10 | Administratietijd | 2 min per toegewezen taak |
| FR12 | Pauze opsplitsen | 2×15 min via flag |
| FR13 | Storingsblok (senior) | ~elke 2 uur incidentblok |
| FR15 | Schilder: binnenwerk bij regen | Regenfilter (>≈50% kans) |
| FR16 | Hitte: extra pauze | +15 min bij >30 °C |

---

## Architectuur

src/
datapunt9/
models.py # Datamodellen (Task, Personnel, Weather, blocks)
rules.py # Pure functies: filters, sortering, helpers
planner.py # Orchestratie algoritme (FR5/8/9/11/14 + extras)
weather_api.py # Open-Meteo client (zonder API-key)
acceptance.py # Formatter naar acceptatie-JSON
io_adapters.py # JSON I/O helpers
app.py # CLI entrypoint
tests/
test_rules.py
test_planner.py
test_weather.py
fixtures/ # voorbeeld JSON voor taken & personeel
config/
settings.example.toml
requirements.txt

**Principes:** scheiding van concerns, pure functies voor testbaarheid, Pydantic type-veiligheid, PEP8.

---

## Installatie

```bash
python -V  # verwacht 3.11+
pip install -r requirements.txt

Gebruik
Genereer een dagtakenlijst voor één medewerker:
python app.py \
  --personeel tests/fixtures/personeel_piet.json \
  --taken tests/fixtures/tasks.json \
  --out output/dagtaken_piet.json \
  --lat 52.37 --lon 4.90   # (optioneel) Amsterdam, beïnvloedt weerregels

--lat/--lon zijn optioneel. Zonder locatie draait het algoritme met “onbekend weer” (graceful fallback).
--out is het JSON-bestand conform acceptatieformat.

Configuratie
Weer-API: Standaard wordt Open-Meteo gebruikt (geen key nodig).
Je kunt config/settings.toml toevoegen als je later providers of drempels wilt wisselen (zie settings.example.toml als start).

Voorbeeldoutput
{
  "personeelsgegevens": {
    "Naam": "Piet de Jong",
    "Werktijd": 240,
    "Beroepstype": "Mechanisch Monteur",
    "Bevoegdheid": "Senior",
    "Specialist_in_attracties": ["Mega Spin", "River Rapids", "Twister"],
    "Pauze_opsplitsen": false,
    "Max_fysieke_belasting": 40
  },
  "weergegevens": { "temperatuur": 20, "kans_op_regen": 30 },
  "dagtaken": [
    { "omschrijving": "Hoge prio spec", "duur": 45, "prioriteit": "Hoog", "beroepstype": "Mechanisch Monteur", "bevoegdheid": "Senior", "attractie": "Twister", "is_buitenwerk": true },
    { "omschrijving": "Hoge prio", "duur": 120, "prioriteit": "Hoog", "beroepstype": "Mechanisch Monteur", "bevoegdheid": "Senior", "is_buitenwerk": false },
    { "omschrijving": "Pauze", "duur": 30 },
    { "omschrijving": "Administratietijd", "aantal_taken": 2, "duur": 4 }
  ],
  "totale_duur": 199
}

Testen

Draai alle tests:
pytest -q

Wat wordt getest:
Unit: grenswaarden fysieke belasting, filtering op profiel, sortering prio/specialisme.
Planner: geen overschrijding werktijd; pauzes/administratie aanwezig; hitte-regel.
Weer-API: interface met mocking (geen echte netwerkcall in unit tests).

Coverage uitbreiden? Voeg pytest-cov toe en draai:
pytest --maxfail=1 --disable-warnings -q --cov=src --cov-report=term-missing

Kwaliteit (rubric)

Leesbaarheid: duidelijke namen, docstrings, type hints, PEP8, geen duplicatie.
Functies: één verantwoordelijkheid per functie; pure functions voor regels.
REST & API: robuuste client met foutafhandeling/fallback.
Testrapportage: beschrijf per FR de testcases + resultaat (geslaagd/gefaald) en verwijs naar relevante tests.

Git-werkwijze
Aanbevolen branching:

main – stabiel

dp9-codekwaliteit – implementatie van DP9

Voorbeeld commits:

feat: FR14 weather client + graceful fallback

feat: FR8 priority & specialism sorting

feat: FR5/FR9 allocation break to avoid overtime

feat: FR11/FR12 pause handling

feat: FR7/FR10/FR13/FR15/FR16 rules

test: unit & integration

docs: README + usage
