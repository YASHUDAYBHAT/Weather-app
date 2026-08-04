# 🌦 Weather App

A modern desktop Weather Application built with **Python**, **PyQt6**, and the **OpenWeatherMap API**. This application provides real-time weather information for any city with a clean glassmorphism-inspired user interface.

---

## 📸 Preview

> Enter a city name, click **Get Weather**, and instantly view the current weather conditions along with a weather icon.

---

## ✨ Features

* 🌍 Search weather by city name
* 🌡 Displays current temperature in Celsius
* ☁ Shows current weather description
* 😊 Displays weather emoji based on conditions
* 🎨 Modern glassmorphism user interface
* ⚡ Fast API response using OpenWeatherMap
* 🔐 API key stored securely using a `.env` file

---

## 🛠 Tech Stack

* Python 3.x
* PyQt6
* Requests
* Python-dotenv
* OpenWeatherMap API

---

## 📂 Project Structure

```text
Weather-App/
│── weather.py
│── .env
│── requirements.txt
│── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/weather-app.git
cd weather-app
```

### 2. Create a virtual environment (Optional)

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install PyQt6 requests python-dotenv
```

---

## 🔑 API Setup

Create a `.env` file in the project root.

```env
API_KEY=YOUR_OPENWEATHERMAP_API_KEY
```

Get your free API key from:

https://openweathermap.org/api

---

## ▶ Running the Application

```bash
python weather.py
```

---

## 📌 How It Works

1. Enter the name of a city.
2. Click **Get Weather**.
3. The application sends a request to the OpenWeatherMap API.
4. The API returns the current weather data.
5. The application displays:

   * Current temperature
   * Weather description
   * Matching weather emoji

---

## 🌈 Weather Icons

| Weather Condition | Emoji |
| ----------------- | ----- |
| Clear Sky         | ☀️    |
| Few Clouds        | ⛅     |
| Cloudy            | ☁️    |
| Rain              | 🌧️   |
| Snow              | ❄️    |
| Unknown           | 🌈    |

---

## 📦 Dependencies

```text
PyQt6
requests
python-dotenv
```

---

## 🔮 Future Improvements

* Animated weather backgrounds
* Rain, snow, and cloud animations
* Thunderstorm effects
* Weather forecast for upcoming days
* Humidity display
* Wind speed information
* Feels-like temperature
* Atmospheric pressure
* Sunrise and sunset timings
* Auto-detect current location
* Search history
* Dark and light mode
* Better weather icons

---

## 🐞 Error Handling

The application handles:

* Invalid city names
* Missing API key
* API request failures
* Network-related errors

---

## 👨‍💻 Author

**Yash Bhat**

Built with Python, PyQt6, and the OpenWeatherMap API.

---

## 📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute this project for educational and personal purposes.
