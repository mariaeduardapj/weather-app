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
search_history = []
city_entry = None
search_button = None
weather_gif_label = None
city_label = None
temp_label = None
desc_label = None
feel_label = None
humidity_label = None
max_min_label = None
toggle_btn = None
forecast_frame = None
history_frame = None
history_labels = []
scrollable_container = None
app = None 

def get_city():
    api_token = os.getenv("API_TOKEN")
    if not api_token:
        print("Erro: API_TOKEN não configurado no arquivo .env")
        return None
    url = f'https://ipinfo.io/json?token={api_token}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('city')
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter cidade por IP: {e}")
        return None
    
def update_search_history(city):
    if not city or city in search_history:
        return
    
    search_history.insert(0, city)
    if len(search_history) > 5:
        search_history.pop()

    for label in history_labels:
        label.destroy()
    history_labels.clear()

    for city_name in search_history:
        label = ctk.CTkButton(
            history_frame,
            text=city_name,
            font=("Tahoma", 12),
            width=1,
            corner_radius=10,
            fg_color="#e0e0e0",
            text_color="#333",
            hover_color="#d0d0d0",
            command=lambda c=city_name: on_history_click(c)
        )
        label.pack(side="left", padx=5)
        history_labels.append(label)

def on_history_click(city_name):
    if city_entry:
        city_entry.delete(0, END)
        city_entry.insert(0, city_name)
    get_weather()

def get_weather():
    city = city_entry.get().strip() if city_entry else ""
    if not city:
        city = get_city()
        if city:
            if city_entry:
                city_entry.delete(0, END)
                city_entry.insert(0, city)
        else:
            if desc_label: desc_label.configure(text="Could not detect city.")
            return

    api_key = os.getenv("API_KEY")
    if not api_key:
        if desc_label: desc_label.configure(text="API_KEY não configurada!")
        return

    current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"
    try:
        response = requests.get(current_weather_url)
        response.raise_for_status()
        data = response.json()

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        desc_display = desc.capitalize()
        feels = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]

        if temp_label: temp_label.configure(text=f"{temp:.1f}°C")
        if desc_label: desc_label.configure(text=f"{desc_display}")
        if city_label: city_label.configure(text=f"{city} 📍")
        if feel_label: feel_label.configure(text=f"Feels like {feels:.1f}°C")
        if humidity_label: humidity_label.configure(text=f"Humidity: {humidity}%")
        if max_min_label: max_min_label.configure(text=f"Min: {temp_min}°C | Max: {temp_max}°C")

        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        try:
            icon_response = requests.get(icon_url)
            icon_response.raise_for_status()
            icon_img = Image.open(BytesIO(icon_response.content)).resize((100, 100))
            icon_tk = ImageTk.PhotoImage(icon_img)
            if weather_gif_label:
                weather_gif_label.configure(image=icon_tk)
                weather_gif_label.image = icon_tk
        except requests.exceptions.RequestException as e:
            print(f"Erro ao carregar ícone: {e}")
            if weather_gif_label: weather_gif_label.configure(image=None)
            if weather_gif_label: weather_gif_label.image = None
        except Exception as e:
            print(f"Erro ao processar imagem do ícone: {e}")
            if weather_gif_label: weather_gif_label.configure(image=None)
            if weather_gif_label: weather_gif_label.image = None

    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter clima atual: {e}")
        if city_label: city_label.configure(text="")
        if temp_label: temp_label.configure(text="")
        if feel_label: feel_label.configure(text="")
        if max_min_label: max_min_label.configure(text="")
        if humidity_label: humidity_label.configure(text="")
        if desc_label: desc_label.configure(text="City not found or API error.")
        if weather_gif_label: weather_gif_label.configure(image=None)
        if weather_gif_label: weather_gif_label.image = None

    for row in forecast_rows:
        row.destroy()
    forecast_rows.clear()

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=en"
    try:
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter previsão: {e}")
        forecast_data = None

    if forecast_data and forecast_data.get("cod") == "200" and forecast_frame:
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
            if count >= 7:
                break
            item = daily_forecasts[date]
            temp_day = item['main']['temp']
            desc_day = item['weather'][0]['description'].capitalize()
            weekday = date.strftime("%A")

            row_frame = ctk.CTkFrame(forecast_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=30, pady=1)

            label_day = ctk.CTkLabel(row_frame, text=weekday, font=("Tahoma", 12, "bold"), width=90, anchor="w")
            label_day.pack(side="left")

            label_temp = ctk.CTkLabel(row_frame, text=f"{temp_day:.0f}°C", font=("Tahoma", 12), width=40, anchor="center")
            label_temp.pack(side="left")

            label_desc = ctk.CTkLabel(row_frame, text=f"|  {desc_day}", font=("Tahoma", 12), anchor="w")
            label_desc.pack(side="left", fill="x", expand=True)

            forecast_rows.append(row_frame)
            count += 1
    
    update_search_history(city)

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
    global history_frame, history_labels
    global scrollable_container, app

    for widget in app.winfo_children():
        widget.destroy()

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    scrollable_container = ctk.CTkScrollableFrame(app, fg_color="transparent")
    scrollable_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    scrollable_container.grid_columnconfigure(0, weight=1)
    scrollable_container.grid_rowconfigure(0, weight=1)

    center_frame = ctk.CTkFrame(scrollable_container, fg_color="transparent")
    center_frame.grid(row=0, column=0)
    center_frame.grid_columnconfigure(0, weight=1)

    main_content_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
    main_content_frame.grid(row=0, column=0, sticky="n")
    main_content_frame.grid_columnconfigure(0, weight=1)

    top_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
    top_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
    top_frame.grid_columnconfigure(0, weight=1)

    city_entry = ctk.CTkEntry(top_frame, placeholder_text="Enter city", font=("Tahoma", 14))
    city_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

    search_button = ctk.CTkButton(top_frame, text="🔍", width=50, command=get_weather)
    search_button.grid(row=0, column=1, padx=(0, 5))

    toggle_btn = ctk.CTkButton(
        top_frame,
        text="🌙" if "pink" in current_theme_path["value"] else "☀️",
        width=50,
        command=toggle_theme
    )
    toggle_btn.grid(row=0, column=2)

    history_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
    history_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")

    info_frame = ctk.CTkFrame(main_content_frame)
    info_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
    info_frame.grid_columnconfigure(1, weight=1)

    weather_gif_label = ctk.CTkLabel(info_frame, text="")
    weather_gif_label.grid(row=0, column=0, padx=(0, 15), sticky="n")

    text_info_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    text_info_frame.grid(row=0, column=1, sticky="nsew")
    for i in range(6):
        text_info_frame.grid_rowconfigure(i, weight=1)

    temp_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 48, "bold"), anchor="w")
    temp_label.grid(row=0, column=0, sticky="w")

    desc_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 14), anchor="w")
    desc_label.grid(row=1, column=0, sticky="w")

    city_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 22, "bold"), anchor="w")
    city_label.grid(row=2, column=0, sticky="w")

    feel_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 18), anchor="w")
    feel_label.grid(row=3, column=0, sticky="w")

    humidity_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 14), anchor="w")
    humidity_label.grid(row=4, column=0, sticky="w")

    max_min_label = ctk.CTkLabel(text_info_frame, text="", font=("Tahoma", 14), anchor="w")
    max_min_label.grid(row=5, column=0, sticky="w")

    forecast_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
    forecast_frame.grid(row=3, column=0, padx=10, pady=(10, 20), sticky="ew")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme(current_theme_path["value"])

app = ctk.CTk()
app.geometry("350x500")
app.title("Weather App ☁️")
app.resizable(True, True)

rebuild_ui()
get_weather()

app.mainloop()