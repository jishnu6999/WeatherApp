from flask import Flask, render_template, request, jsonify, send_file
from pymongo import MongoClient
import requests
import os
import csv, io
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# === API Keys & DB ===
API_KEY = os.getenv("OPENWEATHER_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
GEODB_KEY = os.getenv("GEODB_API_KEY")
GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")

client = MongoClient(MONGO_URI)
db = client.weather_app
data_collection = db.weather_data

# === Helpers ===
def fetch_weather_data(location):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
            "icon": data["weather"][0]["icon"]
        }
    except Exception as e:
        print(f"❌ Error fetching current weather: {e}")
        return None

def fetch_forecast_data(location):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        forecast_list = []
        for i in range(0, len(data["list"]), 8):  # every 24 hours
            entry = data["list"][i]
            forecast_list.append({
                "date": entry["dt_txt"].split(" ")[0],
                "temp": entry["main"]["temp"],
                "desc": entry["weather"][0]["description"]
            })
        return forecast_list
    except Exception as e:
        print(f"❌ Error fetching forecast: {e}")
        return None

# === Routes ===
@app.route('/')
def index():
    return render_template('index.html', google_maps_key=GOOGLE_MAPS_KEY)

@app.route('/weather', methods=['POST'])
def get_weather():
    try:
        location = request.form.get('location')
        if not location:
            return jsonify({'error': 'No location provided'}), 400

        print(f"🌍 Location input: {location}")
        current = fetch_weather_data(location)
        forecast = fetch_forecast_data(location)

        if current and forecast:
            result = {
                "location": location,
                "current": current,
                "forecast": forecast,
                "timestamp": datetime.utcnow().isoformat(),
                "lat": current["lat"],
                "lon": current["lon"]
            }
            data_collection.insert_one(result)
            result.pop("_id", None)
            return jsonify(result)
        else:
            return jsonify({"error": "Failed to fetch weather data"}), 500
    except Exception as e:
        print("❌ Server error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/read')
def read_entries():
    entries = list(data_collection.find({}, {"_id": 0}))
    return jsonify(entries)

@app.route('/update', methods=['POST'])
def update_entry():
    old_location = request.form.get('old_location')
    new_location = request.form.get('new_location')

    updated_data = fetch_weather_data(new_location)
    if not updated_data:
        return jsonify({"error": "Invalid new location"}), 400

    result = data_collection.update_many(
        {"location": old_location},
        {"$set": {"location": new_location, "current": updated_data}}
    )
    return jsonify({"message": "Updated", "modified": result.modified_count})

@app.route('/delete', methods=['POST'])
def delete_entry():
    location = request.form.get('location')
    result = data_collection.delete_many({"location": location})
    return jsonify({"message": "Deleted", "count": result.deleted_count})

@app.route('/youtube')
def youtube_videos():
    city = request.args.get("city")
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{city} travel guide",
        "type": "video",
        "key": YOUTUBE_KEY,
        "maxResults": 3
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return jsonify(res.json()["items"])
    except Exception as e:
        print("❌ YouTube API error:", e)
        return jsonify([])

@app.route('/export/json')
def export_json():
    entries = list(data_collection.find({}, {"_id": 0}))
    return jsonify(entries)

@app.route('/export/csv')
def export_csv():
    entries = list(data_collection.find({}, {"_id": 0}))
    if not entries:
        return "No data to export", 400

    si = io.StringIO()
    writer = csv.DictWriter(si, fieldnames=entries[0].keys())
    writer.writeheader()
    writer.writerows(entries)
    return send_file(io.BytesIO(si.getvalue().encode()), download_name="weather.csv", as_attachment=True)

@app.route('/autocomplete')
def autocomplete():
    city = request.args.get("city")
    if not city:
        return jsonify([])

    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/cities?namePrefix={city}&limit=5"
    headers = {
        "x-rapidapi-key": GEODB_KEY,
        "x-rapidapi-host": "wft-geo-db.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify([c["name"] for c in data["data"]])
    except Exception as e:
        print("❌ GeoDB error:", e)
        return jsonify([])

if __name__ == "__main__":
    app.run(debug=True)
