# 🌦️ Weather App

A simple weather application built with Python and Tkinter to display real-time weather data.  
It connects to the [OpenWeatherMap API](https://openweathermap.org/) to show the current temperature and weather description based on the city entered by the user.

---

## 🧰 Technologies Used

- [Python 3.10+](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – GUI
- [Requests](https://pypi.org/project/requests/) – HTTP requests
- [python-dotenv](https://pypi.org/project/python-dotenv/) – Environment variable loader
- [OpenWeatherMap API](https://openweathermap.org/api)

---

## 📷 Screenshot

![Main screen](midias/main-screen.png)
![Result screen](midias/result-screen.png)

## 🚀 How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/weather-app.git
   cd weather-app

2. Install the dependencies:
    pip install -r requirements.txt

3. Create a .env file with your API key:
    API_KEY=your_api_key_here

4. Run the application:
    python weather_app.py

---

## 💡 Features

- Get current weather by typing a city name
- Display temperature (°C) and weather description 
- Lightweight desktop GUI using Tkinter
- API key protection via .env file

---

## ✨ Possible Improvements

- Show weather icons
- Improve layout with grid() or ttk
- Add multi-day forecast (3 or 5 days)
- Web version with Streamlit

---

## 📁 Project Structure

weather-app/
├── assets/
│   ├── clear.gif
│   └── ...
├── themes/
│   └── pink-theme.json
│   └── dark-theme.json
├── .env
├── weather_app.py
├── README.md
└── requirements.txt

---

## 📄 License

This project is licensed under the MIT License.

