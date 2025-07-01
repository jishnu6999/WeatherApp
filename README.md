
# 🌦️ Advanced Weather App

- **Author:** Jishnuvardhan Karpuram
- **Walkthrough Video:** [Recorded Walkthrough Video of my Project](https://drive.google.com/file/d/1RZl7_J399ZJ1GT9mA1NLuzzkGZJOq6wE/view)
- **Overview:** A full-stack, feature-rich weather application built using **Flask**, **MongoDB**, **Vanilla JavaScript**, **HTML** styled with **Tailwind CSS**, **python**. It allows users to search for weather data by city name or current geolocation, view a 5-day forecast, watch relevant YouTube travel videos, and visualize the location on a Google Map. This project was developed as part of the **PM Accelerator** program.

---

## 🌟 Features

- 🌍 Search by city, zip code, or landmark
- 📍 Geolocation support (use my location)
- 🌡️ Current weather display with icon, temperature, humidity, wind speed
- 📆 5-Day Forecast + ⏱️ Hourly forecast
- 📹 Embedded YouTube travel videos
- 🗺️ Google Maps city visualization
- 🔄 Full CRUD support via MongoDB
- 🧠 Autocomplete city search with GeoDB
- 📤 Export weather data in JSON, CSV, PDF
- 🌗 Modern dark UI with Tailwind CSS
- 🔒 Secure API key management using `.env`

---

## 📂 Project Structure

```
weather_app_advanced/
│
├── app.py                  # Flask backend, all routes and logic
├── .env                    # Environment variables (API keys, Mongo URI)
├── requirements.txt        # Python dependencies
│
├── templates/
│   └── index.html          # Main HTML frontend template (Jinja2)
│
├── static/
│   ├── script.js           # JavaScript for frontend behavior
│   └── style.css (optional)
├── screenshots/            #screenshots of working weather page
│   ├── main_page.png
├── .gitignore              #gitignore file created while doing git push
└── README.md               # Project documentation (this file)
```

---

## 🚀 How It Works

### 1. `app.py` (Flask Backend)

- Handles routing (`/`, `/weather`, `/youtube`, `/autocomplete`, `/export/*`)
- Fetches weather and forecast data from **OpenWeatherMap API**
- Retrieves video data from **YouTube Data API**
- Embeds map using **Google Maps Embed API**
- Connects to **MongoDB Atlas** for storing past searches
- Supports exporting weather entries in JSON, CSV formats
- Includes auto-suggestion support using **GeoDB API**

### 2. `index.html` (Frontend UI)

- Built with **Tailwind CSS**
- Dynamic UI updated via `script.js`
- Sections include:
  - Search Bar + Geolocation button
  - Weather result panel
  - Forecast grid
  - Travel videos
  - Google map
  - About modal popup

### 3. `script.js` (Client-Side Logic)

- Handles form submissions and geolocation
- Sends AJAX requests to Flask routes
- Updates UI with results (current weather, forecast, map, videos)
- Includes autocomplete functionality

### 4. `.env` (Secure API Keys)

Contains sensitive keys used by the backend:

```
OPENWEATHER_API_KEY=7c5a57b1633774911ed4f78b2af4c9a2
YOUTUBE_API_KEY=AIzaSyCKpujyvsmkT-6EZuKfypVEfEvlorSkZL4
GOOGLE_MAPS_KEY=AIzaSyDYSoaekmxUuQukDsKcBpAABVpxtyk2RKU
GEODB_API_KEY=ff877b57fdmsh4105283cd4c871cp136c5cjsnda42ea21c1b8
MONGO_URI=mongodb+srv://Nikhitha:Nikki%402005@cluster0.rwunmqw.mongodb.net/weather_db?retryWrites=true&w=majority&appName=Cluster0

```

---

## 🧪 Technologies Used

| Stack            | Technology              |
|------------------|--------------------------|
| Backend          | Flask (Python)           |
| Frontend         | HTML, Tailwind CSS       |
| Database         | MongoDB Atlas            |
| APIs Used        | OpenWeatherMap, YouTube, Google Maps, GeoDB |
| Deployment Ready | Gunicorn, Heroku/AWS/Fly.io compatible |

---

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7+
- Git
- MongoDB Atlas account
- API keys (see `.env`)

### Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/weather_app_advanced.git
cd weather_app_advanced
```

### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add `.env` file

Create a `.env` in the root:

```env
# Weather and Backend
OPENWEATHER_API_KEY=7c5a57b1633774911ed4f78b2af4c9a2
MONGO_URI=mongodb+srv://Nikhitha:Nikki%402005@cluster0.rwunmqw.mongodb.net/weather_db?retryWrites=true&w=majority&appName=Cluster0

# Google Maps Embed API Key
GOOGLE_MAPS_KEY=AIzaSyDYSoaekmxUuQukDsKcBpAABVpxtyk2RKU

# GeoDB Cities API Key (from RapidAPI)
GEODB_API_KEY=ff877b57fdmsh4105283cd4c871cp136c5cjsnda42ea21c1b8

# YouTube Data API v3 Key
YOUTUBE_API_KEY=AIzaSyCKpujyvsmkT-6EZuKfypVEfEvlorSkZL4
```

### Run the app

```bash
python app.py
```

App will run on `http://127.0.0.1:5000`

---

## 📸 Screenshots

| Search UI | Forecast & Map & Youtube |
|-----------|----------------|
| ![search](screenshots/main_page.png) | ![forecast](screenshots/forecast_maps_yotube.png) |

---

## 🌐 APIs Used

| API              | Description                          |
|------------------|--------------------------------------|
| OpenWeatherMap   | Current and 5-day forecast           |
| GeoDB            | City autocomplete suggestions       |
| YouTube Data API | City-related travel videos          |
| Google Maps Embed| Map embedding for cities            |

---

## 📧 Contact

Built with ❤️ by **Jishnuvardhan Karpuram**  
[LinkedIn](www.linkedin.com/in/jishnuvardhan-karpuram) • [GitHub](https://github.com/jishnu6999/)

---

## 🧠 Acknowledgements

- PM Accelerator Team 🚀  
- MongoDB Communities  
- OpenWeatherMap, GeoDB Cities, Mongo, YouTube & Google Maps APIs
