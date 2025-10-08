from __future__ import annotations
import argparse
from datapunt9.io_adapters import load_personnel_from_json, load_tasks_from_json, write_output_json
from datapunt9.weather_api import WeatherClient
from datapunt9.models import Weather
from datapunt9.planner import genereer_dagtakenlijst
from datapunt9.acceptance import to_acceptance_json
from datapunt9.rules import bereken_max_belasting




def main():
ap = argparse.ArgumentParser()
ap.add_argument("--personeel", required=True)
ap.add_argument("--taken", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--lat", type=float, required=False)
ap.add_argument("--lon", type=float, required=False)
args = ap.parse_args()


p = load_personnel_from_json(args.personeel)
taken = load_tasks_from_json(args.taken)


weather = Weather()
if args.lat is not None and args.lon is not None:
wc = WeatherClient()
wr = wc.fetch(args.lat, args.lon)
weather.temperatuur = wr.temperatuur
weather.kans_op_regen = wr.kans_op_regen


dag = genereer_dagtakenlijst(p, taken, weather)


payload = to_acceptance_json(p, weather, dag)
# Max belasting in personeelsgegevens invullen
payload["personeelsgegevens"]["Max_fysieke_belasting"] = bereken_max_belasting(p.leeftijd, p.verlaagde_fysieke_belasting)


write_output_json(args.out, payload)
print(f"Geschreven: {args.out}")




if __name__ == "__main__":
main()
