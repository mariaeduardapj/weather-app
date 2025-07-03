import customtkinter as ctk
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather():
    city = city_entry.get()
    api_key = os.getenv("API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt_br"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        feels = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]

        temp_result.configure(text=f"{city} ☀️\n{temp:.1f}°C")
        feel.configure(text=f"Feels like {feels:.1f}°C")
        max_min.configure(text=f"Min: {temp_min}°C | Max: {temp_max}°C")
        humidity.configure(text=f"Humidity: {humidity}%")
    else:
        result.configure(text="City not found.")

# ✅ Ordem corrigida:
ctk.set_appearance_mode("light")

app = ctk.CTk()
app.geometry("400x300")
app.title("Weather App ☁️")
app.resizable(False, False)

ctk.set_default_color_theme("themes/pink-theme.json")  # <- agora depois de CTk()

city_entry = ctk.CTkEntry(app, placeholder_text="Enter city", width=250, font=("Arial", 14))
city_entry.pack(pady=10)

search_button = ctk.CTkButton(app, text="Search Weather", command=get_weather, font=("Arial", 14))
search_button.pack(pady=0)

humidity = ctk.CTkLabel(app, text="", font=("Arial", 13), justify="center")
humidity.pack(pady=20)
max_min = ctk.CTkLabel(app, text="", font=("Arial", 13), justify="center")
max_min.pack(pady=20)
temp_result = ctk.CTkLabel(app, text="", font=("Arial", 13), justify="center")
temp_result.pack(pady=20)
feel = ctk.CTkLabel(app, text="", font=("Arial", 13), justify="center")
feel.pack(pady=20)
result = ctk.CTkLabel(app, text="", font=("Arial", 13), justify="center")
result.pack(pady=20)

app.mainloop()
