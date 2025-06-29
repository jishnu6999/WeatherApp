document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("weatherForm");
  const locationInput = document.getElementById("location");
  const result = document.getElementById("result");
  const cityName = document.getElementById("cityName");
  const weatherInfo = document.getElementById("weatherInfo");
  const forecastContainer = document.getElementById("forecast");
  const hourlyForecastContainer = document.getElementById("hourlyForecast");
  const videosContainer = document.getElementById("videos");
  const mapFrame = document.getElementById("map");
  const geoBtn = document.getElementById("geoBtn");

  async function fetchWeather(location) {
    try {
      const response = await fetch("/weather", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `location=${encodeURIComponent(location)}`
      });

      const data = await response.json();
      if (data.error) throw new Error(data.error);

      // Display city name
      cityName.textContent = `Weather in ${data.location}`;

      // Show current weather
      const current = data.current;
      weatherInfo.innerHTML = `
        <img src="https://openweathermap.org/img/wn/${current.icon || "01d"}@2x.png" alt="${current.description}" class="inline-block w-10 h-10 align-middle mr-2" />
        <span>${current.description}, ${current.temperature}°C</span><br>
        <span>Humidity: ${current.humidity}%, Wind: ${current.wind_speed} m/s</span>
      `;

      // Display hourly forecast (if backend supports it in future)
      if (Array.isArray(data.hourly)) {
        hourlyForecastContainer.innerHTML = "";
        data.hourly.slice(0, 8).forEach((h) => {
          const div = document.createElement("div");
          div.className = "p-2 bg-gray-700 rounded";
          div.textContent = `${h.time}: ${h.temp}°C`;
          hourlyForecastContainer.appendChild(div);
        });
      }

      // Display 5-day forecast
      forecastContainer.innerHTML = "";
      data.forecast.forEach((f) => {
        const div = document.createElement("div");
        div.className = "p-2 bg-gray-700 rounded";
        div.textContent = `${f.date}: ${f.desc}, ${f.temp}°C`;
        forecastContainer.appendChild(div);
      });

      // Embed Google Map
      if (mapFrame && data.lat && data.lon) {
        mapFrame.src = `https://www.google.com/maps/embed/v1/place?key=${GOOGLE_MAPS_KEY}&q=${data.lat},${data.lon}`;
      }

      // Load travel videos from YouTube
      videosContainer.innerHTML = "";
      const ytResp = await fetch(`/youtube?city=${encodeURIComponent(data.location)}`);
      const videos = await ytResp.json();
      videos.forEach((v) => {
        const iframe = document.createElement("iframe");
        iframe.src = `https://www.youtube.com/embed/${v.id.videoId}`;
        iframe.width = "100%";
        iframe.height = "200";
        iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        iframe.allowFullscreen = true;
        videosContainer.appendChild(iframe);
      });

      result.classList.remove("hidden");
    } catch (err) {
      alert("❌ Failed to load weather data: " + err.message);
    }
  }

  // Submit via form
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const location = locationInput.value.trim();
    if (location) fetchWeather(location);
  });

  // Geolocation support
  geoBtn.addEventListener("click", () => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(async (pos) => {
        const { latitude, longitude } = pos.coords;
        try {
          const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
          const data = await res.json();
          const city = data.address.city || data.address.town || data.address.state || "Your Location";
          locationInput.value = city;
          fetchWeather(city);
        } catch {
          alert("Could not resolve your location");
        }
      }, () => {
        alert("Location access denied.");
      });
    } else {
      alert("Geolocation not supported in this browser.");
    }
  });
});
