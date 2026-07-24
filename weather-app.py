import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
import os
import dotenv

dotenv.load_dotenv()

class weatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter the city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.show_temperature_label = QLabel("", self)
        self.emojis_label = QLabel("", self)
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Weather App")
        layout = QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.show_temperature_label)
        layout.addWidget(self.emojis_label)
        self.setLayout(layout)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        city = self.city_input.text()
        api_key = os.getenv("API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
            weather_description = data['weather'][0]['description']
            if "clear" in weather_description or "sunny" in weather_description or "sun" in weather_description:
                emoji = "☀️"
            elif "clouds" in weather_description or "overcast" in weather_description:
                emoji = "☁️"
            elif "broken clouds" in weather_description or "few clouds" in weather_description:
                emoji = "⛅"
            elif "rains" in weather_description or "drizzle" in weather_description or "shower" in weather_description or "thunderstorm" in weather_description or "rain" in weather_description:
                emoji = "🌧️"
            elif "snow" in weather_description or "sleet" in weather_description or "blizzard" in weather_description:
                emoji = "❄️"
            else:
                emoji = "🌈"
            
            self.show_temperature_label.setText(f"The current temperature in {city} is {temperature:.2f}°C with {weather_description}.")
            self.emojis_label.setText(f"Weather Emoji: {emoji}")
        else:
          self.show_temperature_label.setText(f"city noot found. Please check the city name and try again.")
          self.emojis_label.setText("❌")
          
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = weatherApp()
    window.show()
    sys.exit(app.exec())