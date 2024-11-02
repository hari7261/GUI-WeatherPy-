 # 🌐 FutureWeather: A Modern Weather App

Welcome to **FutureWeather**, a sleek and intuitive weather application built using Python's Tkinter library! This application fetches real-time weather data from the OpenWeatherMap API, providing users with accurate and up-to-date information in an attractive interface.

## 📸 Screenshot
![Screenshot 2024-11-02 233243](https://github.com/user-attachments/assets/d5b9402a-06ed-4dc9-b4cd-94e90a95e5e6)

## 🚀 Features

- **Real-Time Weather Data**: Fetch current weather and 5-day forecast based on user input.
- **Dynamic Icon Loading**: Real-time loading of weather icons with caching for fast access.
- **User-Friendly GUI**: Built using Tkinter for a modern, responsive interface.
- **Light & Dark Mode**: Toggle between light and dark themes for comfortable viewing.
- **Automatic Updates**: Weather data updates every 5 minutes for the latest information.

## 🛠️ Technologies Used

| Technology        | Description                                |
|-------------------|--------------------------------------------|
| **Python 3.x**    | Programming language used for development  |
| **Tkinter**       | GUI toolkit for creating the interface     |
| **OpenWeatherMap API** | Source for real-time weather data      |
| **Pillow**        | Python Imaging Library for handling icons  |

## 📦 Installation

To set up the FutureWeather application on your local machine, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/futureweather.git
   cd futureweather
   ```

2. **Install Required Packages**:
   ```bash
   pip install requests Pillow customtkinter
   ```

3. **Add Your API Key**:
   - Replace `"YOUR_API_KEY"` in `weather_app.py` with your actual OpenWeatherMap API key.

4. **Run the Application**:
   ```bash
   python weather_app.py
   ```

## ⚙️ Usage

1. **Enter a City Name**: Type the name of the city in the input field.
2. **Click Search**: Hit the "Search" button to fetch the weather data.
3. **Toggle Units**: Switch between Celsius and Fahrenheit.
4. **Switch Themes**: Toggle between light and dark modes for a personalized experience.

## 🌍 Icon Guide

| Weather Condition  | Icon | Emoji |
|---------------------|------|-------|
| Clear Sky           | ![Clear](https://openweathermap.org/img/wn/01d@2x.png) | ☀️ |
| Few Clouds          | ![Few Clouds](https://openweathermap.org/img/wn/02d@2x.png) | 🌤️ |
| Scattered Clouds     | ![Scattered Clouds](https://openweathermap.org/img/wn/03d@2x.png) | ⛅ |
| Broken Clouds       | ![Broken Clouds](https://openweathermap.org/img/wn/04d@2x.png) | 🌥️ |
| Shower Rain         | ![Shower Rain](https://openweathermap.org/img/wn/09d@2x.png) | 🌧️ |
| Rain                | ![Rain](https://openweathermap.org/img/wn/10d@2x.png) | 🌧️ |
| Thunderstorm        | ![Thunderstorm](https://openweathermap.org/img/wn/11d@2x.png) | ⛈️ |
| Snow                | ![Snow](https://openweathermap.org/img/wn/13d@2x.png) | ❄️ |
| Mist                | ![Mist](https://openweathermap.org/img/wn/50d@2x.png) | 🌫️ |


---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

### 🌟 Thank you for checking out FutureWeather! Stay tuned for more features and updates! 🌟
