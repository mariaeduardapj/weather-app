import tkinter as tk
import requests
import os
from dotenv import load_dotenv
from PIL import Image, ImageTk

load_dotenv()

gif_frames=[]
gif_delay=0
gif_label=None

def play_gif(label, frames, delay, current_frame_index=0):
    if not frames:
        return
    frame = frames[current_frame_index]
    label.config(image=frame)
    current_frame_index=(current_frame_index+1) % len(frames)
    label.after(delay, play_gif, label, frames, delay, current_frame_index)

def load_gif(file_path):
    global gif_frames, gif_delay
    try:
        image=Image.open(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return False
    except Exception as e:
        print(f"Error loading GIF: {e}")
        return False
    temp_frames=[]
    try:
        while True:
            temp_frames.append(ImageTk.PhotoImage(image.copy()))
            image.seek(len(temp_frames))
    except EOFError:
        pass
    gif_frames=temp_frames
    gif_delay=image.info.get('duration',100)
    return True

def get_weather():
    city = city_entry.get()
    api_key = os.getenv("API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt_br"

    response = requests.get(url)         
    data = response.json()               

    if response.status_code == 200:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        result_label.config(text=f"{city} - {temp}°C\n{desc.capitalize()}")
    else:
        result_label.config(text="City not found.")

root = tk.Tk()
root.title("Weather App 🌦️")
root.geometry("400x400")
root.configure(bg="#ffe6f0")

gif_file="C:\\Users\\duda2\\Estudos\\Projetos\\weather-app\\f.gif"
if load_gif(gif_file):
    gif_label=tk.Label(root,bg="#ffe6f0")
    gif_label.pack(pady=10)
    play_gif(gif_label, gif_frames, gif_delay)
else:
    error_gif_label=tk.Label(root, text="Could not load GIF",bg="#ffe6f0")
    error_gif_label.pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 14), bg="#ffffff")
city_entry.pack(pady=15)

btn = tk.Button(
    root,
    text=" Check Weather ", 
    font=("Arial",12,"bold"),
    bg="#ff99cc",
    fg="#ffffff",
    activebackground="#ff66b2",
    activeforeground="#ffffff",
    bd=0,
    command=get_weather)
btn.pack()


result_label = tk.Label(root, font="Arial, 12")
result_label.pack(pady=20)

root.mainloop()