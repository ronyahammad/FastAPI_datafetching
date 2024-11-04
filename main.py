import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase
service_account_key = json.loads(os.getenv("FIREBASE_KEY"))
cred = credentials.Certificate(service_account_key)  
firebase_admin.initialize_app(cred)

db = firestore.client()

app = FastAPI()

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 36.9898,
    "longitude": 7.921066,
    "hourly": ["temperature_2m", "relative_humidity_2m", "surface_pressure","vapour_pressure_deficit", "wind_speed_10m", "soil_temperature_0cm"],
    "timezone": "auto"
}

@app.get("/fetch-weather-data")
async def fetch_weather_data():
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        try:
            # Create a Firestore document with the current timestamp
            doc_ref = db.collection("weather_data").document(datetime.now().isoformat())
            doc_ref.set({
                "timestamp": datetime.now().isoformat(),
                "temperature_2m": data["hourly"]["temperature_2m"][-1],
                "relative_humidity_2m": data["hourly"]["relative_humidity_2m"][-1],
                "surface_pressure": data["hourly"]["surface_pressure"][-1],
                "vapour_pressure_deficit": data["hourly"]["vapour_pressure_deficit"][-1],
                "wind_speed_10m": data["hourly"]["wind_speed_10m"][-1],
                "soil_temperature_0cm": data["hourly"]["soil_temperature_0cm"][-1]
            })
            return {"message": "Weather data saved successfully"}
        except KeyError:
            raise HTTPException(status_code=500, detail="Unexpected data format from API response.")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from API")

@app.get("/get-weather-data")
async def get_weather_data():
    try:
        docs = db.collection("weather_data").stream()
        data = [{doc.id: doc.to_dict()} for doc in docs]
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
