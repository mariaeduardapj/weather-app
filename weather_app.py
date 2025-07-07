import customtkinter as ctk
import requests
import os
from tkinter import END
from dotenv import load_dotenv
from PIL import Image, ImageTk
from datetime import datetime
from io import BytesIO

load_dotenv()

current_theme_path = {"value": "themes/pink-theme.json"}
forecast_rows = []
forecast_frame = None

def get_city():
    api_token = os.getenv("API_TOKEN")
    url = f'https://ipinfo.io/json?token={api_token}'
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('city')
    except:
        return None

def get_weather():
    city = city_entry.get().strip()
    if not city:
        city = get_city()
        if city:
            city_entry.delete(0, END)
            city_entry.insert(0, city)
        else:
            desc_label.configure(text="Could not detect city.")
            return

    api_key = os.getenv("API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        desc_display = desc.capitalize()
        feels = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]

        temp_label.configure(text=f"{temp:.1f}°C")
        desc_label.configure(text=f"{desc_display}")
        city_label.configure(text=f"{city} 📍")
        feel_label.configure(text=f"Feels like {feels:.1f}°C")
        humidity_label.configure(text=f"Humidity: {humidity}%")
        max_min_label.configure(text=f"Min: {temp_min}°C | Max: {temp_max}°C")

        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        try:
            icon_response = requests.get(icon_url)
            icon_img = Image.open(BytesIO(icon_response.content)).resize((100, 100))
            icon_tk = ImageTk.PhotoImage(icon_img)
            weather_gif_label.configure(image=icon_tk)
            weather_gif_label.image = icon_tk
        except:
            weather_gif_label.configure(image=None)
            weather_gif_label.image = None
    else:
        city_label.configure(text="")
        temp_label.configure(text="")
        feel_label.configure(text="")
        max_min_label.configure(text="")
        humidity_label.configure(text="")
        desc_label.configure(text="City not found.")
        weather_gif_label.configure(image=None)
        weather_gif_label.image = None

    for row in forecast_rows:
        row.destroy()
    forecast_rows.clear()

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=en"
    try:
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
    except:
        forecast_data = None

    if forecast_data and forecast_data.get("cod") == "200":
        daily_forecasts = {}
        for item in forecast_data['list']:
            dt_txt = item['dt_txt']
            try:
                date = datetime.fromisoformat(dt_txt).date()
            except ValueError:
                continue
            if date not in daily_forecasts:
                daily_forecasts[date] = item

        sorted_dates = sorted(daily_forecasts.keys())
        count = 0
        for date in sorted_dates:
            if date == datetime.now().date():
                continue
            if count >= 3:
                break
            item = daily_forecasts[date]
            temp_day = item['main']['temp']
            desc_day = item['weather'][0]['description'].capitalize()
            weekday = date.strftime("%A")

            row_frame = ctk.CTkFrame(forecast_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=2)

            label_day = ctk.CTkLabel(row_frame, text=weekday, font=("Tahoma", 12), width=110, anchor="w")
            label_day.pack(side="left")

            label_temp = ctk.CTkLabel(row_frame, text=f"{temp_day:.0f}°C", font=("Tahoma", 12), width=40, anchor="center")
            label_temp.pack(side="left")

            label_desc = ctk.CTkLabel(row_frame, text=f"|  {desc_day}", font=("Tahoma", 12), anchor="w")
            label_desc.pack(side="left")

            forecast_rows.append(row_frame)
            count += 1

def toggle_theme():
    if "pink" in current_theme_path["value"]:
        current_theme_path["value"] = "themes/dark-theme.json"
    else:
        current_theme_path["value"] = "themes/pink-theme.json"

    ctk.set_default_color_theme(current_theme_path["value"])
    rebuild_ui()

def rebuild_ui():
    global city_entry, search_button, weather_gif_label
    global city_label, temp_label, desc_label
    global feel_label, humidity_label, max_min_label
    global toggle_btn, forecast_frame

    for widget in app.winfo_children():
        widget.destroy()

    city_entry = ctk.CTkEntry(app, placeholder_text="Enter city", width=250, font=("Tahoma", 14))
    city_entry.pack(pady=10)

    search_button = ctk.CTkButton(app, text="Search Weather", command=get_weather, font=("Tahoma", 14))
    search_button.pack(pady=0)

    toggle_btn = ctk.CTkButton(app, text="🌙" if "pink" in current_theme_path["value"] else "☀️", width=30, command=toggle_theme)
    toggle_btn.place(x=310, y=10)

    info_frame = ctk.CTkFrame(app)
    info_frame.pack(pady=20, padx=20, fill="x")

    weather_gif_label = ctk.CTkLabel(info_frame, text="")
    weather_gif_label.pack(side="left", padx=(0, 15), anchor="n")

    text_info_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    text_info_frame.pack(side="left", fill="x", expand=True)

    temp_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 48, "bold"))
    temp_label.pack(pady=(0, 0), anchor='w')

    desc_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 14), justify="left")
    desc_label.pack(pady=(0, 0), anchor='w')

    city_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 22, "bold"), justify="left")
    city_label.pack(pady=(10, 0), anchor='w')

    feel_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 18), justify="left")
    feel_label.pack(pady=(0, 0), anchor='w')

    humidity_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 14), justify="left")
    humidity_label.pack(pady=(0, 0), anchor='w')

    max_min_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 14), justify="left")
    max_min_label.pack(pady=(0, 0), anchor='w')

    forecast_frame = ctk.CTkFrame(app, fg_color="transparent")
    forecast_frame.pack(pady=(5, 10), fill="x")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme(current_theme_path["value"])

app = ctk.CTk()
app.geometry("350x500")
app.title("Weather App ☁️")
app.resizable(False, False)

rebuild_ui()
get_weather()
app.mainloop()
