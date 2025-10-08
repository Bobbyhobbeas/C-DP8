from datapunt9.weather_api import WeatherClient


# Alleen smoke-test van de interface (geen echte call hier)


def test_weather_interface_smoke(monkeypatch):
def fake_fetch(self, lat, lon):
class R: pass
return type("W", (), {"temperatuur": 20, "kans_op_regen": 40})()
monkeypatch.setattr(WeatherClient, "fetch", fake_fetch)
wc = WeatherClient()
r = wc.fetch(0, 0)
assert r.temperatuur == 20 and r.kans_op_regen == 40
