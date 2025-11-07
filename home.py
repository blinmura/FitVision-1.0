from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import json
import os
import subprocess
from progress_manager import ProgressManager  # ✅ используем твой класс

# --- Настройки окна ---
root = Tk()
window_width = 400
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.configure(bg="#232323")
root.title("Workout Plan")
root.overrideredirect(True)

# --- Верхняя панель ---
title_bar = Frame(root, bg="#232323", relief="raised", bd=2, borderwidth=0, highlightthickness=0)
title_bar.pack(side=TOP, fill=X)
Label(title_bar, text="Workout Plan", fg="white", bg="#232323", font=("Verdana", 9, "bold")).pack(side=LEFT, padx=10)

def back_to_dashboard():
    root.destroy()
    print("Возврат к dashboard.py")
    subprocess.Popen([".venv\\Scripts\\python", "dashboard.py"], shell=True)

Button(title_bar, text="✕", fg="white", bg="#232323", font=("Verdana", 9, "bold"),
       command=back_to_dashboard, borderwidth=0, highlightthickness=0).pack(side=RIGHT, padx=5, pady=2)

# --- Данные и цели ---
exercise_goals = {
    "PushUp": 100,
    "Squat": 20,
    "Lunges": 20,
    "Plank": 60,  # в секундах
    "ShoulderTap": 20
}

# --- Получаем текущего пользователя ---
current_user = ProgressManager.get_current_user()
print(f"Текущий пользователь: {current_user}")

# --- Загружаем его персональный прогресс ---
progress_data = ProgressManager.load_progress()
print("Загруженный прогресс:", progress_data)

# --- Проверяем, если файл пуст или нового пользователя нет, создаем пустой прогресс ---
if not progress_data:
    ProgressManager.reset_user_progress()
    progress_data = {}

# --- Список упражнений ---
exercises = [
    {"name": "PushUp", "desc": "100 Push up a day", "image": "push_up.jpg", "level": "Intermediate"},
    {"name": "Squat", "desc": "20 Sit up a day", "image": "squats.jpg", "level": "Beginner"},
    {"name": "Lunges", "desc": "20 Lunges a day", "image": "lunges.jpg", "level": "Beginner"},
    {"name": "Plank", "desc": "60 second Plank a day", "image": "plank.jpg", "level": "Beginner"},
    {"name": "ShoulderTap", "desc": "20 Shoulder Tap a day", "image": "shoulder_tap.jpg", "level": "Beginner"},
]

progress_bars = {}
progress_labels = {}

# --- Функции ---
def on_card_click(exercise_name):
    print(f"Вы нажали на: {exercise_name}")
    command = [".venv\\Scripts\\python", "FitVision.py", "--type", exercise_name.lower(), "--source", "0"]
    subprocess.Popen(command, shell=True)
    print(f"Запущено упражнение: {exercise_name}")

def on_enter(e):
    e.widget.config(bg="#E0E0E0")

def on_leave(e):
    e.widget.config(bg="white")

def update_progress(exercise, value):
    """Обновление и визуализация прогресса"""
    progress_data[exercise] = min(exercise_goals[exercise], progress_data.get(exercise, 0) + value)
    progress_percent = (progress_data[exercise] / exercise_goals[exercise]) * 100

    progress_bars[exercise]["value"] = progress_percent
    progress_labels[exercise]["text"] = f"{int(progress_percent)}%"

    if progress_percent >= 100:
        progress_labels[exercise].config(bg="green")
    elif progress_percent >= 50:
        progress_labels[exercise].config(bg="yellow")
    else:
        progress_labels[exercise].config(bg="red")

    # ✅ сохраняем индивидуально для текущего пользователя
    ProgressManager.save_progress(exercise, progress_data[exercise])

def create_exercise_card(parent, exercise):
    """Создание карточки упражнения"""
    card = Frame(parent, bg="white", bd=0, relief="flat", cursor="hand2")
    card.pack(fill="x", padx=20, pady=20)

    if os.path.exists(exercise["image"]):
        img = Image.open(exercise["image"]).resize((80, 80), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
    else:
        img = None

    img_label = Label(card, image=img, bg="white")
    img_label.image = img
    img_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

    Label(card, text=exercise["name"], font=("Arial", 12, "bold"), bg="white").grid(row=0, column=1, sticky="w")
    Label(card, text=exercise["desc"], font=("Arial", 10), fg="gray", bg="white").grid(row=1, column=1, sticky="w")
    Label(card, text=exercise["level"], font=("Arial", 9, "bold"), fg="white", bg="black", padx=8, pady=2).grid(row=0, column=2, padx=10, sticky="e")

    progress_frame = Frame(card, bg="white")
    progress_frame.grid(row=2, column=1, columnspan=2, sticky="ew", pady=5)

    current_progress = progress_data.get(exercise["name"], 0)
    percent = (current_progress / exercise_goals[exercise["name"]]) * 100 if exercise["name"] in progress_data else 0

    progress_label = Label(progress_frame, text=f"{int(percent)}%", font=("Arial", 9, "bold"), fg="white", bg="green", padx=8)
    progress_label.pack(side=LEFT, padx=5)
    progress_labels[exercise["name"]] = progress_label

    progress = ttk.Progressbar(progress_frame, length=200, value=percent, mode="determinate")
    progress.pack(fill="x", expand=True)
    progress_bars[exercise["name"]] = progress

    card.bind("<Button-1>", lambda e: on_card_click(exercise["name"]))
    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)

# --- Создаём карточки ---
for ex in exercises:
    create_exercise_card(root, ex)

root.mainloop()
