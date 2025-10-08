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
