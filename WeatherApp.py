
import customtkinter as ctk
import requests
from PIL import Image, ImageTk
import json
from datetime import datetime, timedelta
import os
from pathlib import Path
import threading
import time
import io
import urllib.request
from math import ceil

class WeatherApp:
    def __init__(self):
        self.API_KEY = ""
        self.window = ctk.CTk()
        self.window.title("Python Weather App")
        self.window.geometry("1000x800")
        self.window.resizable(True, True)
        
        # Set the color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.temp_unit = "C"
        self.setup_ui()
        self.current_city = "Salem"  
        self.update_thread = None
        self.running = True
        self.weather_icons = {}
        
    def setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Top control panel
        self.control_panel = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.control_panel.pack(fill="x", pady=(0, 20))
        
        # Search frame (left side of control panel)
        self.search_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.search_frame.pack(side="left")
        
        self.city_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Enter city name...",
            width=300,
            height=40,
            font=("Helvetica", 14)
        )
        self.city_entry.pack(side="left", padx=(0, 10))
        
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=100,
            height=40,
            command=self.update_weather,
            font=("Helvetica", 14)
        )
        self.search_button.pack(side="left")
        
        # Unit toggle and theme controls (right side of control panel)
        self.controls_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.controls_frame.pack(side="right")
        
        self.unit_button = ctk.CTkButton(
            self.controls_frame,
            text="°C / °F",
            width=80,
            command=self.toggle_unit,
            font=("Helvetica", 14)
        )
        self.unit_button.pack(side="left", padx=5)
        
        self.theme_button = ctk.CTkButton(
            self.controls_frame,
            text="Theme",
            width=80,
            command=self.toggle_theme,
            font=("Helvetica", 14)
        )
        self.theme_button.pack(side="left", padx=5)
        
        # Current weather frame
        self.weather_frame = ctk.CTkFrame(self.main_frame)
        self.weather_frame.pack(fill="x", pady=(0, 20))
        
        # City name and time
        self.city_label = ctk.CTkLabel(
            self.weather_frame,
            text="Loading...",
            font=("Helvetica", 32, "bold")
        )
        self.city_label.pack(pady=(20, 0))
        
        self.time_label = ctk.CTkLabel(
            self.weather_frame,
            text="",
            font=("Helvetica", 14)
        )
        self.time_label.pack()
        
        # Current weather icon
        self.weather_icon_label = ctk.CTkLabel(
            self.weather_frame,
            text="",  # Will be replaced with image
            font=("Helvetica", 48)
        )
        self.weather_icon_label.pack(pady=(10, 0))
        
        # Temperature
        self.temp_label = ctk.CTkLabel(
            self.weather_frame,
            text="--°C",
            font=("Helvetica", 48, "bold")
        )
        self.temp_label.pack()
        
        # Feels like temperature
        self.feels_like_label = ctk.CTkLabel(
            self.weather_frame,
            text="Feels like: --°C",
            font=("Helvetica", 16)
        )
        self.feels_like_label.pack()
        
        # Weather description
        self.desc_label = ctk.CTkLabel(
            self.weather_frame,
            text="--",
            font=("Helvetica", 18)
        )
        self.desc_label.pack()
        
        # Detailed weather info
        self.details_frame = ctk.CTkFrame(self.weather_frame)
        self.details_frame.pack(fill="x", pady=20, padx=40)
        
        for i in range(4):
            self.details_frame.grid_columnconfigure(i, weight=1)
        
        # Weather details
        details = [
            ("Humidity", "--"),
            ("Wind Speed", "--"),
            ("Pressure", "--"),
            ("Visibility", "--")
        ]
        
        self.detail_labels = {}
        for i, (label, value) in enumerate(details):
            self.detail_labels[label] = ctk.CTkLabel(
                self.details_frame,
                text=f"{label}\n{value}",
                font=("Helvetica", 16),
            )
            self.detail_labels[label].grid(row=0, column=i, padx=10, pady=10)
        
        # Forecast frame
        self.forecast_frame = ctk.CTkFrame(self.main_frame)
        self.forecast_frame.pack(fill="both", expand=True)
        
        self.forecast_label = ctk.CTkLabel(
            self.forecast_frame,
            text="5-Day Forecast",
            font=("Helvetica", 24, "bold")
        )
        self.forecast_label.pack(pady=(20, 10))
        
        # Container for forecast cards
        self.forecast_container = ctk.CTkFrame(self.forecast_frame, fg_color="transparent")
        self.forecast_container.pack(fill="x", padx=20, pady=10)
        
        for i in range(5):
            self.forecast_container.grid_columnconfigure(i, weight=1)
        
        # Create empty forecast cards
        self.forecast_cards = []
        for i in range(5):
            card = self.create_forecast_card(i)
            self.forecast_cards.append(card)
            
    def create_forecast_card(self, index):
        card = ctk.CTkFrame(self.forecast_container)
        card.grid(row=0, column=index, padx=5, pady=5, sticky="nsew")
        
        date_label = ctk.CTkLabel(card, text="--", font=("Helvetica", 14))
        date_label.pack(pady=(10, 5))
        
        icon_label = ctk.CTkLabel(card, text="")
        icon_label.pack(pady=5)
        
        temp_label = ctk.CTkLabel(card, text="--°C", font=("Helvetica", 18, "bold"))
        temp_label.pack(pady=5)
        
        desc_label = ctk.CTkLabel(card, text="--", font=("Helvetica", 12))
        desc_label.pack(pady=(0, 10))
        
        return {
            "frame": card,
            "date": date_label,
            "icon": icon_label,
            "temp": temp_label,
            "desc": desc_label
        }
        
    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "light" if current_mode == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        
    def toggle_unit(self):
        self.temp_unit = "F" if self.temp_unit == "C" else "C"
        self.update_weather()
        
    def convert_temp(self, celsius):
        if self.temp_unit == "C":
            return f"{ceil(celsius)}°C"
        return f"{ceil((celsius * 9/5) + 32)}°F"
        
    def load_weather_icon(self, icon_code):
        if icon_code in self.weather_icons:
            return self.weather_icons[icon_code]
            
        try:
            url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            response = urllib.request.urlopen(url)
            image_data = response.read()
            image = Image.open(io.BytesIO(image_data))
            photo = ImageTk.PhotoImage(image)
            self.weather_icons[icon_code] = photo
            return photo
        except Exception as e:
            print(f"Error loading weather icon: {e}")
            return None
            
    def update_time(self):
        while self.running:
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.configure(text=current_time)
            time.sleep(1)
            
    def get_weather_data(self, city):
        try:
            # Current weather
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_KEY}&units=metric"
            current_response = requests.get(current_url)
            current_data = current_response.json()
            
            # Forecast
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.API_KEY}&units=metric"
            forecast_response = requests.get(forecast_url)
            forecast_data = forecast_response.json()
            
            if current_response.status_code == 200 and forecast_response.status_code == 200:
                # Process current weather
                current_weather = {
                    "temperature": current_data["main"]["temp"],
                    "feels_like": current_data["main"]["feels_like"],
                    "humidity": current_data["main"]["humidity"],
                    "pressure": current_data["main"]["pressure"],
                    "wind_speed": current_data["wind"]["speed"],
                    "visibility": current_data["visibility"] // 1000,  # Convert to km
                    "description": current_data["weather"][0]["description"].capitalize(),
                    "icon": current_data["weather"][0]["icon"],
                    "city": current_data["name"]
                }
                
                # Process forecast data (get one forecast per day)
                forecasts = []
                seen_dates = set()
                
                for item in forecast_data["list"]:
                    date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
                    if date not in seen_dates and len(forecasts) < 5:
                        seen_dates.add(date)
                        forecasts.append({
                            "date": datetime.fromtimestamp(item["dt"]).strftime("%a, %b %d"),
                            "temp": item["main"]["temp"],
                            "description": item["weather"][0]["description"].capitalize(),
                            "icon": item["weather"][0]["icon"]
                        })
                
                return current_weather, forecasts
            else:
                return None, None
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None, None
            
    def update_weather(self):
        city = self.city_entry.get() if self.city_entry.get() else self.current_city
        current_weather, forecasts = self.get_weather_data(city)
        
        if current_weather and forecasts:
            self.current_city = city
            
            # Update current weather
            self.city_label.configure(text=current_weather["city"])
            self.temp_label.configure(text=self.convert_temp(current_weather["temperature"]))
            self.feels_like_label.configure(text=f"Feels like: {self.convert_temp(current_weather['feels_like'])}")
            self.desc_label.configure(text=current_weather["description"])
            
            # Update weather icon
            icon_image = self.load_weather_icon(current_weather["icon"])
            if icon_image:
                self.weather_icon_label.configure(image=icon_image)
                self.weather_icon_label.image = icon_image
            
            # Update details
            self.detail_labels["Humidity"].configure(text=f"Humidity\n{current_weather['humidity']}%")
            self.detail_labels["Wind Speed"].configure(text=f"Wind Speed\n{current_weather['wind_speed']} m/s")
            self.detail_labels["Pressure"].configure(text=f"Pressure\n{current_weather['pressure']} hPa")
            self.detail_labels["Visibility"].configure(text=f"Visibility\n{current_weather['visibility']} km")
            
            # Update forecast cards
            for card, forecast in zip(self.forecast_cards, forecasts):
                card["date"].configure(text=forecast["date"])
                card["temp"].configure(text=self.convert_temp(forecast["temp"]))
                card["desc"].configure(text=forecast["description"])
                
                icon_image = self.load_weather_icon(forecast["icon"])
                if icon_image:
                    card["icon"].configure(image=icon_image)
                    card["icon"].image = icon_image
            
            # Schedule next update
            self.window.after(300000, self.update_weather)
        else:
            self.city_label.configure(text="City not found")
            
    def run(self):
        # Start the time update thread
        self.update_thread = threading.Thread(target=self.update_time, daemon=True)
        self.update_thread.start()
        
        # Initial weather update
        self.update_weather()
        
        # Start the main loop
        self.window.mainloop()
        
        # Clean up
        self.running = False
        if self.update_thread:
            self.update_thread.join()

if __name__ == "__main__":
    app = WeatherApp()
    app.run()
