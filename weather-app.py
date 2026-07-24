import sys
import requests
from PyQt6.QtWidgets import QApplication, QFrame, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
import os
import dotenv

dotenv.load_dotenv()

class weatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter the city name:")
        self.city_input = QLineEdit()

        self.get_weather_button = QPushButton("Get Weather")

        self.emojis_label = QLabel("")
        self.weather_label = QLabel("")
        self.temperature_label = QLabel("")

        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emojis_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("🌦 Weather App")
        self.setFixedSize(500, 550)

        # Glass Card
        self.card = QFrame()
        self.card.setObjectName("glassCard")

        card_layout = QVBoxLayout()
        card_layout.setSpacing(18)
        card_layout.setContentsMargins(30, 30, 30, 30)

        card_layout.addWidget(self.city_label)
        card_layout.addWidget(self.city_input)
        card_layout.addWidget(self.get_weather_button)

        card_layout.addSpacing(10)

        card_layout.addWidget(self.emojis_label)
        card_layout.addWidget(self.weather_label)
        card_layout.addWidget(self.temperature_label)

        self.card.setLayout(card_layout)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.card)
        layout.addStretch()

        self.setLayout(layout)

        self.get_weather_button.clicked.connect(self.get_weather)

        self.setStyleSheet("""
        QWidget{
            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:1,
                stop:0 #1E3C72,
                stop:1 #2A5298
            );
            font-family:'Segoe UI';
        }

        QFrame#glassCard{
            background:rgba(255,255,255,0.15);
            border:1px solid rgba(255,255,255,0.30);
            border-radius:25px;
        }

        QLabel{
            color:white;
            background:transparent;
        }

        QLineEdit{
            background:rgba(255,255,255,0.18);
            border:2px solid rgba(255,255,255,0.35);
            border-radius:15px;
            padding:10px;
            font-size:16px;
            color:white;
        }

        QLineEdit:focus{
            border:2px solid #6DD5FA;
        }

        QPushButton{
            background:rgba(52,152,219,0.75);
            color:white;
            border:none;
            border-radius:15px;
            padding:12px;
            font-size:17px;
            font-weight:bold;
        }

        QPushButton:hover{
            background:rgba(52,152,219,0.95);
        }

        QPushButton:pressed{
            background:#1F618D;
        }
        """)

        self.city_label.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            background:transparent;
        """)

        self.emojis_label.setStyleSheet("""
            font-size:90px;
            background:transparent;
        """)

        self.weather_label.setStyleSheet("""
            font-size:28px;
            font-weight:600;
            background:transparent;
        """)
        self.weather_label.setWordWrap(True)

        self.temperature_label.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            background:transparent;
        """)
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
            
            self.temperature_label.setText(f"The current temperature in {city} is {temperature:.2f}°C with {weather_description}.")
            self.emojis_label.setText(f"Current Weather: {emoji}")
        else:
          self.temperature_label.setText(f"city not found. Please check the city name and try again.")
          self.emojis_label.setText("❌")
          
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = weatherApp()
    window.show()
    sys.exit(app.exec())