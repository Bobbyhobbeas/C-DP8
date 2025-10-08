from __future__ import annotations
from typing import List
import json
from .models import Task, Personnel




def load_tasks_from_json(path: str) -> List[Task]:
with open(path, "r", encoding="utf-8") as f:
data = json.load(f)
return [Task(**row) for row in data]




def load_personnel_from_json(path: str) -> Personnel:
with open(path, "r", encoding="utf-8") as f:
data = json.load(f)
return Personnel(**data)




def write_output_json(path: str, payload: dict) -> None:
with open(path, "w", encoding="utf-8") as f:
json.dump(payload, f, ensure_ascii=False, indent=2)
