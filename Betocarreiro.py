import tkinter as tk
from PIL import Image, ImageTk
import requests
import time
import random
import threading
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def fetch_wait_times():
    url = "https://queue-times.com/parks/319/queue_times.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rides = data['rides']
            return rides
        else:
            print(f"Failed to fetch data: HTTP status code {response.status_code}")
            return []
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

def update_attraction_info(label, background_label, root, images):
    image_keys = list(images.keys())
    while True:
        rides = fetch_wait_times()
        if rides:
            random.shuffle(rides)
            for ride in rides:
                name = ride['name']
                wait_time = ride.get('wait_time', 0)
                status = "Closed" if not ride['is_open'] else f"{wait_time} min wait"
                text = f"{name}: {status}"
                label.config(text=text)

                random_image_key = random.choice(image_keys)
                background_label.config(image=images[random_image_key])

                root.update_idletasks()
                time.sleep(10)
        else:
            label.config(text="No ride information available.")
            print("No rides data returned from the API.")
            time.sleep(10)

def create_gui():
    root = tk.Tk()
    root.title("Beto Carrero Wait Times")

    window_width = 300
    window_height = 100

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_right = int(screen_width - window_width - 10)
    position_down = int(screen_height - window_height - 50)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

    root.attributes('-topmost', True)

    # Load background images numbered from 1 to 6
    images = {str(i): ImageTk.PhotoImage(Image.open(resource_path(f"{i}.jpg")).resize((window_width, window_height), Image.Resampling.LANCZOS)) for i in range(1, 7)}

    background_label = tk.Label(root)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    text_label = tk.Label(root, font=("Helvetica", 10), fg="white", bg="black", wraplength=window_width-20)
    text_label.place(relx=0.5, rely=0.5, anchor='center')

    threading.Thread(target=update_attraction_info, args=(text_label, background_label, root, images), daemon=True).start()

    root.mainloop()

create_gui()
