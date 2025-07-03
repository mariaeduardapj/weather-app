import customtkinter as ctk
import requests
import os
from dotenv import load_dotenv
from PIL import Image, ImageTk

load_dotenv()

WEATHER_GIFS = {
    "clear sky": "assets/clear.gif",
    "few clouds": "assets/clouds.gif",
    "scattered clouds": "assets/clouds.gif",
    "broken clouds": "assets/clouds.gif",
    "overcast clouds": "assets/clouds.gif",
    "shower rain": "assets/rain.gif",
    "rain": "assets/rain.gif",
    "thunderstorm": "assets/thunderstorm.gif",
    "snow": "assets/snow.gif",
    "mist": "assets/mist.gif",
    "smoke": "assets/mist.gif",
    "haze": "assets/mist.gif",
    "dust": "assets/mist.gif",
    "fog": "assets/mist.gif",
    "sand": "assets/mist.gif",
    "ash": "assets/mist.gif",
    "squall": "assets/mist.gif",
    "tornado": "assets/tornado.gif"
}

gif_frames_cache = {}
gif_animation_jobs = {}
current_theme_path = {"value": "themes/pink-theme.json"}

def load_gif_frame(path, frame_index, size=(100, 100)):
    try:
        img = Image.open(path)
        img.seek(frame_index)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except:
        return None

def animate_gif(label, gif_path, frame_index=0):
    if gif_path not in gif_frames_cache:
        frames = []
        img = Image.open(gif_path)
        try:
            while True:
                frames.append(ImageTk.PhotoImage(img.resize((100, 100), Image.LANCZOS)))
                img.seek(img.tell() + 1)
        except EOFError:
            pass
        gif_frames_cache[gif_path] = frames

    frames = gif_frames_cache[gif_path]
    if not frames:
        return

    frame = frames[frame_index]
    label.configure(image=frame)
    label.image = frame

    next_frame_index = (frame_index + 1) % len(frames)

    if gif_animation_jobs.get(label):
        app.after_cancel(gif_animation_jobs[label])

    job_id = app.after(100, animate_gif, label, gif_path, next_frame_index)
    gif_animation_jobs[label] = job_id

def get_weather():
    city = city_entry.get()
    api_key = os.getenv("API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"

    response = requests.get(url)
    data = response.json()

    if gif_animation_jobs.get(weather_gif_label):
        app.after_cancel(gif_animation_jobs[weather_gif_label])
        gif_animation_jobs[weather_gif_label] = None

    if response.status_code == 200:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        feels = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]

        temp_label.configure(text=f"{temp:.1f}°C")
        desc_label.configure(text=f"{desc}")
        city_label.configure(text=f"{city} 📍")
        feel_label.configure(text=f"Feels like {feels:.1f}°C")
        humidity_label.configure(text=f"Humidity: {humidity}%")
        max_min_label.configure(text=f"Min: {temp_min}°C | Max: {temp_max}°C")

        gif_path = WEATHER_GIFS.get(desc, "assets/default.gif")
        if os.path.exists(gif_path):
            animate_gif(weather_gif_label, gif_path)
        else:
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
    global toggle_btn

    for widget in app.winfo_children():
        widget.destroy()

    city_entry = ctk.CTkEntry(app, placeholder_text="Enter city", width=250, font=("Tahoma", 14))
    city_entry.pack(pady=10)

    search_button = ctk.CTkButton(app, text="Search Weather", command=get_weather, font=("Tahoma", 14))
    search_button.pack(pady=0)

    toggle_btn = ctk.CTkButton(app, text="🌙" if "pink" in current_theme_path["value"] else "☀️", width=30, command=toggle_theme)
    toggle_btn.place(x=310, y=10)

    info_frame = ctk.CTkFrame(app)
    info_frame.pack(pady=20, padx=20, fill="both", expand=True)

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

ctk.set_appearance_mode("light")
ctk.set_default_color_theme(current_theme_path["value"])

app = ctk.CTk()
app.geometry("350x350")
app.title("Weather App ☁️")
app.resizable(False, False)

rebuild_ui()
app.mainloop()