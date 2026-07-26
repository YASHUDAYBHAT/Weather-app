import sys
import random
import requests
from PyQt6.QtWidgets import (
    QApplication, QFrame, QWidget, QVBoxLayout, QStackedLayout,
    QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
import os
import dotenv

dotenv.load_dotenv()


class WeatherBackground(QWidget):
    """Fullscreen animated background: rain / snow / clouds / thunderstorm / clear."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.weather_type = "clear"
        self.particles = []
        self.flash_alpha = 0  # for thunderstorm lightning flash

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(30)  # ~33 FPS

    def set_weather(self, weather_type: str):
        """weather_type: 'rain', 'snow', 'clouds', 'thunderstorm', or 'clear'"""
        self.weather_type = weather_type
        self.init_particles()

    def init_particles(self):
        w = max(self.width(), 1)
        h = max(self.height(), 1)
        self.particles = []

        if self.weather_type in ("rain", "thunderstorm"):
            for _ in range(110):
                x = random.uniform(0, w)
                y = random.uniform(-h, h)
                speed = random.uniform(14, 26)
                length = random.uniform(10, 18)
                self.particles.append([x, y, speed, length])

        elif self.weather_type == "snow":
            for _ in range(90):
                x = random.uniform(0, w)
                y = random.uniform(-h, h)
                speed = random.uniform(1, 3.2)
                radius = random.uniform(1.5, 4)
                drift = random.uniform(-0.6, 0.6)
                self.particles.append([x, y, speed, radius, drift])

        elif self.weather_type == "clouds":
            for _ in range(6):
                x = random.uniform(-100, w)
                y = random.uniform(20, h * 0.35)
                size = random.uniform(35, 65)
                speed = random.uniform(0.15, 0.45)
                self.particles.append([x, y, size, speed])

    def resizeEvent(self, event):
        self.init_particles()
        super().resizeEvent(event)

    def update_particles(self):
        w = max(self.width(), 1)
        h = max(self.height(), 1)

        if self.weather_type in ("rain", "thunderstorm"):
            for p in self.particles:
                p[1] += p[2]
                if p[1] > h:
                    p[1] = random.uniform(-40, 0)
                    p[0] = random.uniform(0, w)
            if self.weather_type == "thunderstorm":
                if self.flash_alpha > 0:
                    self.flash_alpha = max(0, self.flash_alpha - 25)
                elif random.random() < 0.012:
                    self.flash_alpha = 200

        elif self.weather_type == "snow":
            for p in self.particles:
                p[1] += p[2]
                p[0] += p[4]
                if p[1] > h:
                    p[1] = random.uniform(-20, 0)
                    p[0] = random.uniform(0, w)

        elif self.weather_type == "clouds":
            for p in self.particles:
                p[0] += p[3]
                if p[0] > w + 100:
                    p[0] = -100
                    p[1] = random.uniform(20, h * 0.35)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.weather_type in ("rain", "thunderstorm"):
            pen = QPen(QColor(174, 214, 241, 170))
            pen.setWidth(2)
            painter.setPen(pen)
            for x, y, speed, length in self.particles:
                painter.drawLine(QPointF(x, y), QPointF(x - 3, y + length))

            if self.weather_type == "thunderstorm" and self.flash_alpha > 0:
                painter.fillRect(self.rect(), QColor(255, 255, 255, self.flash_alpha))

        elif self.weather_type == "snow":
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(255, 255, 255, 230)))
            for x, y, speed, radius, drift in self.particles:
                painter.drawEllipse(QPointF(x, y), radius, radius)

        elif self.weather_type == "clouds":
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(255, 255, 255, 35)))
            for x, y, size, speed in self.particles:
                painter.drawEllipse(QPointF(x, y), size, size * 0.55)


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

        centered_layout = QVBoxLayout()
        centered_layout.addStretch()
        centered_layout.addWidget(self.card)
        centered_layout.addStretch()

        # Foreground content widget (transparent, holds the card)
        content = QWidget()
        content.setLayout(centered_layout)
        content.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        content.setStyleSheet("background: transparent;")

        # Animated background widget (rain/snow/clouds/etc)
        self.background = WeatherBackground()

        # Stack background behind content
        stack = QStackedLayout(self)
        stack.setStackingMode(QStackedLayout.StackingMode.StackAll)
        stack.addWidget(self.background)
        stack.addWidget(content)

        self.get_weather_button.clicked.connect(self.get_weather)

        self.setStyleSheet("""
        weatherApp{
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
            font-size:20px;
            font-weight:600;
            background:transparent;
        """)
        self.weather_label.setWordWrap(True)

        self.temperature_label.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            background:transparent;
        """)
        self.temperature_label.setWordWrap(True)

    def get_weather(self):
        city = self.city_input.text().strip()
        api_key = os.getenv("API_KEY")

        # Step 1: resolve the city name to exact coordinates first.
        # City names alone are ambiguous (e.g. "Manali" exists in both
        # Himachal Pradesh and as a Chennai locality) - geocoding first
        # avoids the weather API silently matching the wrong place.
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)

        if geo_response.status_code != 200 or not geo_response.json():
            self.emojis_label.setText("❌")
            self.weather_label.setText("City not found")
            self.temperature_label.setText("Please check the city name and try again.")
            self.background.set_weather("clear")
            return

        geo_data = geo_response.json()[0]
        lat, lon = geo_data["lat"], geo_data["lon"]
        resolved_name = geo_data.get("name", city)
        state = geo_data.get("state", "")
        country = geo_data.get("country", "")
        location_str = ", ".join(part for part in (resolved_name, state, country) if part)

        # Step 2: fetch weather for those exact coordinates.
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']  # already in °C thanks to units=metric
            weather_description = data['weather'][0]['description']
            desc = weather_description.lower()

            if "thunderstorm" in desc:
                emoji = "⛈️"
                self.background.set_weather("thunderstorm")
            elif "snow" in desc or "sleet" in desc or "blizzard" in desc:
                emoji = "❄️"
                self.background.set_weather("snow")
            elif "rain" in desc or "drizzle" in desc or "shower" in desc:
                emoji = "🌧️"
                self.background.set_weather("rain")
            elif "broken clouds" in desc or "few clouds" in desc:
                emoji = "⛅"
                self.background.set_weather("clouds")
            elif "clouds" in desc or "overcast" in desc:
                emoji = "☁️"
                self.background.set_weather("clouds")
            elif "clear" in desc or "sunny" in desc or "sun" in desc:
                emoji = "☀️"
                self.background.set_weather("clear")
            else:
                emoji = "🌈"
                self.background.set_weather("clear")

            self.emojis_label.setText(emoji)
            self.weather_label.setText(f"{location_str}\nCurrent Weather: {weather_description.title()}")
            self.temperature_label.setText(f"The current temperature is {temperature:.2f}°C.")
        else:
            self.emojis_label.setText("❌")
            self.weather_label.setText("Something went wrong")
            self.temperature_label.setText("Please try again.")
            self.background.set_weather("clear")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = weatherApp()
    window.show()
    sys.exit(app.exec())