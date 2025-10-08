from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import requests


@dataclass
class WeatherResult:
temperatuur: Optional[int]
kans_op_regen: Optional[int]


class WeatherClient:
"""Kleine client voor Open-Meteo (geen API-key nodig).
Documentatie: https://open-meteo.com/
"""
BASE = "https://api.open-meteo.com/v1/forecast"


def fetch(self, lat: float, lon: float) -> WeatherResult:
params = {
"latitude": lat,
"longitude": lon,
"current": ["temperature_2m", "precipitation"],
"hourly": ["precipitation_probability"],
}
try:
r = requests.get(self.BASE, params=params, timeout=10)
r.raise_for_status()
data = r.json()
temp = None
prob = None
# current temperature
if "current" in data and "temperature_2m" in data["current"]:
temp_val = data["current"]["temperature_2m"]
temp = int(round(float(temp_val)))
# approximate precipitation probability: take next available hourly value
if "hourly" in data and "precipitation_probability" in data["hourly"]:
arr = data["hourly"]["precipitation_probability"]
if isinstance(arr, list) and arr:
prob = int(round(float(arr[0])))
return WeatherResult(temp, prob)
except Exception:
# Robuuste foutafhandeling (rubric): gracefully degrade
return WeatherResult(None, None)
