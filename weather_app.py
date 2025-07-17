import customtkinter as ctk
import requests
import os
import matplotlib
from tkinter import END
from dotenv import load_dotenv
from PIL import Image, ImageTk
from datetime import datetime
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

load_dotenv()

current_language = {"value": "en"}
lang_alias = {
    "en": "en",
    "fr": "fr",
    "de": "de",
    "it": "it",
    "ja": "ja",
    "kr": "kr",
    "pt": "pt",
    "es": "es",
    "sp": "es"
}
translations = {
    "en": {
        "error_api": "Error: API_TOKEN not set in .env file",
        "enter_city": "Enter city",
        "feels_like": "Feels like {temp}°C",
        "humidity": "Humidity: {humidity}%",
        "min_max": "Min: {min}°C | Max: {max}°C",
        "not_found": "City not found or API error.",
        "detect_fail": "Could not detect city.",
        "weekdays": {
            "Monday": "Monday",
            "Tuesday": "Tuesday",
            "Wednesday": "Wednesday",
            "Thursday": "Thursday",
            "Friday": "Friday",
            "Saturday": "Saturday",
            "Sunday": "Sunday"
        },
        "graph_title": "Today's temperature",
        "graph_xlabel": "Time",
        "graph_ylabel": "°C"
    },
    "fr": {
        "error_api": "Erreur : API_TOKEN non défini dans le fichier .env",
        "enter_city": "Entrez la ville",
        "feels_like": "Ressenti {temp}°C",
        "humidity": "Humidité: {humidity}%",
        "min_max": "Min: {min}°C | Max: {max}°C",
        "not_found": "Ville non trouvée ou erreur API.",
        "detect_fail": "Impossible de détecter la ville.",
        "weekdays": {
            "Monday": "Lundi",
            "Tuesday": "Mardi",
            "Wednesday": "Mercredi",
            "Thursday": "Jeudi",
            "Friday": "Vendredi",
            "Saturday": "Samedi",
            "Sunday": "Dimanche"
        },
        "graph_title": "Température d'aujourd'hui",
        "graph_xlabel": "Heure",
        "graph_ylabel": "°C"
    },
    "de": {
        "error_api": "Fehler: API_TOKEN nicht in der .env-Datei festgelegt",
        "enter_city": "Stadt eingeben",
        "feels_like": "fühlt sich an wie {temp}°C",
        "humidity": "Luftfeuchtigkeit: {humidity}%",
        "min_max": "Min: {min}°C | Max: {max}°C",
        "not_found": "Stadt nicht gefunden oder API-Fehler.",
        "detect_fail": "Stadt konnte nicht erkannt werden.",
        "weekdays": {
            "Monday": "Montag",
            "Tuesday": "Dienstag",
            "Wednesday": "Mittwoch",
            "Thursday": "Donnerstag",
            "Friday": "Freitag",
            "Saturday": "Samstag",
            "Sunday": "Sonntag"
        },
        "graph_title": "Heutige Temperatur",
        "graph_xlabel": "Uhrzeit",
        "graph_ylabel": "°C"
    },
    "it": {
        "error_api": "Errore: API_TOKEN non impostato nel file .env",
        "enter_city": "Inserisci la città",
        "feels_like": "Sembra {temp}°C",
        "humidity": "Umidità: {humidity}%",
        "min_max": "Min: {min}°C | Max: {max}°C",
        "not_found": "Città non trovata o errore API.",
        "detect_fail": "Impossibile rilevare la città.",
        "weekdays": {
            "Monday": "Lunedì",
            "Tuesday": "Martedì",
            "Wednesday": "Mercoledì",
            "Thursday": "Giovedì",
            "Friday": "Venerdì",
            "Saturday": "Sabato",
            "Sunday": "Domenica"
        },
        "graph_title": "Temperatura di oggi",
        "graph_xlabel": "Orario",
        "graph_ylabel": "°C"
    },
    "ja": {
        "error_api": "エラー: API_TOKEN が .env ファイルに設定されていません",
        "enter_city": "都市を入力してください",
        "feels_like": "体感温度: {temp}°C",
        "humidity": "湿度: {humidity}%",
        "min_max": "最低: {min}°C | 最高: {max}°C",
        "not_found": "都市が見つからないか、API エラーです",
        "detect_fail": "都市を検出できませんでした",
        "weekdays": {
            "Monday": "月曜日",
            "Tuesday": "火曜日",
            "Wednesday": "水曜日",
            "Thursday": "木曜日",
            "Friday": "金曜日",
            "Saturday": "土曜日",
            "Sunday": "日曜日"
        },
        "graph_title": "今日の気温",
        "graph_xlabel": "時間",
        "graph_ylabel": "°C"

    },
    "kr": {
        "error_api": "오류: .env 파일에 API_TOKEN이 설정되지 않았습니다.",
        "enter_city": "도시를 입력하세요",
        "feels_like": "체감 온도: {temp}°C",
        "humidity": "습도: {humidity}%",
        "min_max": "최소: {min}°C | 최대: {max}°C",
        "not_found": "도시를 찾을 수 없거나 API 오류가 발생했습니다",
        "detect_fail": "도시를 감지할 수 없습니다",
        "weekdays": {
            "Monday": "월요일",
            "Tuesday": "화요일",
            "Wednesday": "수요일",
            "Thursday": "목요일",
            "Friday": "금요일",
            "Saturday": "토요일",
            "Sunday": "일요일"
        },
        "graph_title": "오늘의 기온",
        "graph_xlabel": "시간",
        "graph_ylabel": "°C"
    },
    "pt": {
        "error_api": "Erro: API_TOKEN não configurado no arquivo .env",
        "enter_city": "Digite a cidade",
        "feels_like": "Sensação térmica {temp}°C",
        "humidity": "Umidade: {humidity}%",
        "min_max": "Mín: {min}°C | Máx: {max}°C",
        "not_found": "Cidade não encontrada ou erro na API.",
        "detect_fail": "Não foi possível detectar a cidade.",
        "weekdays": {
            "Monday": "Segunda-feira",
            "Tuesday": "Terça-feira",
            "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira",
            "Friday": "Sexta-feira",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        },
        "graph_title": "Temperatura de hoje",
        "graph_xlabel": "Horário",
        "graph_ylabel": "°C"
    },
    "es": {
        "error_api": "Error: API_TOKEN no está configurado en el archivo .env",
        "enter_city": "Introduce la ciudad",
        "feels_like": "Se siente como {temp}°C",
        "humidity": "Humedad: {humidity}%",
        "min_max": "Mín: {min}°C | Máx: {max}°C",
        "not_found": "Ciudad no encontrada o error de API.",
        "detect_fail": "No se pudo detectar la ciudad.",
        "weekdays": {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        },
        "graph_title": "Temperatura de hoy",
        "graph_xlabel": "Hora",
        "graph_ylabel": "°C"
    }
}

def t(key, **kwargs):
    lang = lang_alias.get(current_language["value"], "en")
    text = translations[lang].get(key, key)
    return text.format(**kwargs)

def translate_weekday(weekday):
    lang = current_language["value"]
    return translations[lang]["weekdays"].get(weekday, weekday)

current_theme_path = {"value": "themes/pink-theme.json"}
forecast_rows = []
search_history = []
forecast_chart = None
autocomplete_listbox = None
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
        print(t("error_api"))
        return None
    url = f'https://ipinfo.io/json?token={api_token}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('city')
    except requests.exceptions.RequestException as e:
        print(t("not_found"))
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

    text_color = "#ffffff" if "dark" in current_theme_path["value"] else "#d63384"

    for city_name in search_history:
        label = ctk.CTkButton(
            history_frame,
            text=city_name,
            font=("Tahoma", 12),
            width=1,
            corner_radius=10,
            text_color=text_color,
            command=lambda c=city_name: on_history_click(c)
        )
        label.pack(side="left", padx=5)
        history_labels.append(label)

def on_history_click(city_name):
    if city_entry:
        city_entry.delete(0, END)
        city_entry.insert(0, city_name)
    get_weather()

def on_city_keyrelease(event):
    global autocomplete_listbox
    query = city_entry.get().strip()
    if len(query) < 2:
        if autocomplete_listbox:
            autocomplete_listbox.destroy()
        return

    api_key = os.getenv("API_KEY")
    lang = lang_alias.get(current_language["value"], "en")
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={api_key}&lang={lang}"

    try:
        res = requests.get(url)
        res.raise_for_status()
        results = res.json()
    except:
        results = []

    if autocomplete_listbox:
        autocomplete_listbox.destroy()

    if results:
        autocomplete_listbox = ctk.CTkFrame(app, fg_color="#ffffff" if "pink" in current_theme_path["value"] else "#222222", corner_radius=6)
        autocomplete_listbox.place(x=city_entry.winfo_rootx() - app.winfo_rootx(),
                                   y=city_entry.winfo_rooty() - app.winfo_rooty() + city_entry.winfo_height())

        for item in results:
            name = f"{item['name']}, {item.get('state', '')} {item['country']}".strip(', ')
            btn = ctk.CTkButton(autocomplete_listbox, text=name, font=("Tahoma", 12), width=200,
                                command=lambda n=name: select_autocomplete(n))
            btn.pack(padx=5, pady=2)

def select_autocomplete(city_name):
    global autocomplete_listbox
    city_entry.delete(0, END)
    city_entry.insert(0, city_name)
    if autocomplete_listbox:
        autocomplete_listbox.destroy()
    get_weather()

def get_weather():
    city = city_entry.get().strip() if city_entry and city_entry.get() else ""
    if not city:
        city = get_city()
        if city:
            if city_entry:
                city_entry.delete(0, END)
                city_entry.insert(0, city)
        else:
            if desc_label: desc_label.configure(text=t("not_found"))
            return

    api_key = os.getenv("API_KEY")
    if not api_key:
        if desc_label: desc_label.configure(text=t("error_api"))
        return

    lang = lang_alias.get(current_language["value"], "en")
    current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang={lang}"
    try:
        response = requests.get(current_weather_url)
        response.raise_for_status()
        data = response.json()

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        if current_language["value"] in ["en", "fr", "de", "it", "es", "pt"]:
           desc_display = desc.capitalize()
        else:
           desc_display = desc
        feels = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]

        if temp_label: temp_label.configure(text=f"{temp:.1f}°C")
        if desc_label: desc_label.configure(text=f"{desc_display}")
        if city_label: city_label.configure(text=f"{city} 📍")
        if feel_label: feel_label.configure(text=t("feels_like", temp=feels))
        if humidity_label: humidity_label.configure(text=t("humidity", humidity=humidity))
        if max_min_label: max_min_label.configure(text=t("min_max", min=temp_min, max=temp_max))

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
        except:
            if weather_gif_label: weather_gif_label.configure(image=None)
            if weather_gif_label: weather_gif_label.image = None

    except:
        if desc_label: desc_label.configure(text=t("not_found"))

    for row in forecast_rows:
        row.destroy()
    forecast_rows.clear()

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang={lang}"
    try:
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        global forecast_chart
        if forecast_chart:
            forecast_chart.get_tk_widget().destroy()
            forecast_chart = None

        def plot_today_temperatures(data):
            today = datetime.now().date()
            times = []
            temps = []

            for item in data["list"][:8]:  # Pega as 8 primeiras previsões
                dt = datetime.fromisoformat(item["dt_txt"])
                times.append(dt.strftime("%Hh"))
                temps.append(item["main"]["temp"])

            if not times:
                return

            fig = Figure(figsize=(4.2, 2), dpi=100)
            ax = fig.add_subplot(111)
            color = "#ff6699" if "pink" in current_theme_path["value"] else "#cccccc"
            ax.plot(times, temps, marker="o", color=color)
            ax.set_title(t("graph_title"))
            ax.set_ylabel(t("graph_ylabel"))
            ax.set_xlabel(t("graph_xlabel"))
            ax.grid(True)

            global forecast_chart
            forecast_chart = FigureCanvasTkAgg(fig, master=forecast_frame)
            forecast_chart.draw()
            forecast_chart.get_tk_widget().pack(pady=10)
    
        plot_today_temperatures(forecast_data)

    except:
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
            weekday = translate_weekday(date.strftime("%A"))

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
    if toggle_btn:
        toggle_btn.configure(text="🌙" if "pink" in current_theme_path["value"] else "☀️")

def rebuild_ui():
    global city_entry, search_button, weather_gif_label
    global city_label, temp_label, desc_label
    global feel_label, humidity_label, max_min_label
    global toggle_btn, forecast_frame
    global history_frame, history_labels
    global scrollable_container, app

    for widget in app.winfo_children():
        widget.destroy()

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    scrollable_container = ctk.CTkScrollableFrame(app)
    scrollable_container.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    scrollable_container.grid_columnconfigure(0, weight=1)
    scrollable_container.grid_rowconfigure(0, weight=1)
    scrollable_container.grid_rowconfigure(1, weight=0)
    scrollable_container.grid_rowconfigure(2, weight=1)

    main_content_frame = ctk.CTkFrame(scrollable_container, fg_color="transparent")
    main_content_frame.grid(row=1, column=0, sticky="n")
    main_content_frame.grid_columnconfigure(0, weight=1)

    top_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
    top_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
    top_frame.grid_columnconfigure(0, weight=1)
    top_frame.grid_columnconfigure(1, weight=4)
    top_frame.grid_columnconfigure(2, weight=4)
    top_frame.grid_columnconfigure(3, weight=1)

    def change_language(new_lang):
        current_language["value"] = new_lang
        rebuild_ui()

    lang_menu = ctk.CTkOptionMenu(
        top_frame,
        values=["en", "fr", "de", "it", "ja", "kr", "pt", "es"],
        command=change_language,
        width=80
    )
    lang_menu.set(current_language["value"])
    lang_menu.grid(row=0, column=3, padx=(5, 0))
    top_frame.grid_columnconfigure(3, weight=1)


    city_entry = ctk.CTkEntry(top_frame, placeholder_text=t("enter_city"), font=("Tahoma", 14))
    city_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
    city_entry = ctk.CTkEntry(top_frame, placeholder_text=t("enter_city"), font=("Tahoma", 14))
    city_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
    city_entry.bind("<KeyRelease>", on_city_keyrelease)

    search_button = ctk.CTkButton(top_frame, text="🔍", command=get_weather)
    search_button.grid(row=0, column=1, sticky="ew", padx=(0, 5))

    toggle_btn = ctk.CTkButton(top_frame, text="🌙" if "pink" in current_theme_path["value"] else"☀️", command=toggle_theme)
    toggle_btn.grid(row=0, column=2, sticky="ew")

    history_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent", height=30)
    history_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

    info_frame = ctk.CTkFrame(main_content_frame)
    info_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
    info_frame.grid_columnconfigure((0,1), weight=1)

    weather_gif_label = ctk.CTkLabel(info_frame, text="")
    weather_gif_label.grid(row=0, column=0, padx=(0, 15), sticky="n")

    text_info_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    text_info_frame.grid(row=0, column=1, sticky="nsew")
    text_info_frame.grid_columnconfigure(0, weight=1)
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
    forecast_frame.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="ew")

    if search_history:
        update_search_history(search_history[0])



ctk.set_appearance_mode("light")
ctk.set_default_color_theme(current_theme_path["value"])

app = ctk.CTk()
app.geometry("400x600")
app.title("Weather App ☁️")
app.resizable(True, True)

rebuild_ui()
get_weather()

app.mainloop()
