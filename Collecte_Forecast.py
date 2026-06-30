import requests
import pandas as pd
import os
from datetime import datetime
URL = "https://api.weather.com/v3/wx/forecast/hourly/3day"
PARAMS_BASE = {
    "apiKey": os.environ["WEATHER_API_KEY"],  # on ne mettra plus la clé en dur dans le code
    "language": "en-US",
    "units": "m",
    "format": "json",
    "icaoCode": "LFPB",
}

FICHIER = "lfpb_forecast.csv"

def fetch_lfpb():
    r = requests.get(URL, params=PARAMS_BASE, timeout=10)
    if r.status_code != 200:
        print(f"Erreur {r.status_code} -> {r.text}")
        return None
    return r.json()

event = fetch_lfpb()

rows = []

for days in event["dayOfWeek"]:
    j0 = event["days"]
    
    rows.append({
        "time": j0["validTimeLocal"],
        "temperature": j0["temperature"],
    })

data = pd.DataFrame(rows)

if not data.empty:
    data["_collecte_le"] = datetime.now().isoformat()
    data.to_csv(FICHIER, mode="a", header=not os.path.exists(FICHIER), index=False)
    print("Donnée enregistrée")
