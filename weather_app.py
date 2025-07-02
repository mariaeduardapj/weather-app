import tkinter as tk
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
        result_label.config(text=f"{city} - {temp}°C\n{desc.capitalize()}")
    else:
        result_label.config(text="City not found.")

root = tk.Tk()
root.title("Current weather")
root.geometry("300x200")

city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10)

btn = tk.Button(root, text="Search weather", command=get_weather)
btn.pack()

result_label = tk.Label(root, font="Arial, 12")
result_label.pack(pady=20)

root.mainloop()