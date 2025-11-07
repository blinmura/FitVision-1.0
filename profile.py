from tkinter import *
import os
import json
import subprocess

# --- Получение имени пользователя ---
if os.path.exists("accounts.json"):
    with open("accounts.json", "r") as f:
        accounts = json.load(f)
    username = accounts.get("last_logged_in", "User")
else:
    username = "User"

# --- Функция вычисления прогресса пользователя ---
def get_user_progress(username):
    """Возвращает средний процент выполнения всех упражнений для текущего пользователя"""
    if not os.path.exists("progress.json"):
        return 0  # если файл не найден

    with open("progress.json", "r") as f:
        data = json.load(f)

    user_data = data.get(username, {})
    if not user_data:
        return 0

    # Сумма процентов по всем упражнениям
    total = 0
    goals = {
        "PushUp": 100,
        "Squat": 20,
        "Lunges": 20,
        "Plank": 60,
        "ShoulderTap": 20
    }

    for exercise, done in user_data.items():
        if exercise in goals:
            percent = min(done / goals[exercise] * 100, 100)
            total += percent

    avg_progress = total / len(goals)
    return round(avg_progress, 1)

# --- Получаем прогресс текущего пользователя ---
progress_percent = get_user_progress(username)

# --- Определяем сообщение в зависимости от прогресса ---
if progress_percent == 0:
    activity_text = "You haven't started yet 😴"
elif progress_percent < 50:
    activity_text = "You're getting started 💪 Keep it up!"
elif progress_percent < 100:
    activity_text = f"Halfway there! ({progress_percent}%) 🚀"
else:
    activity_text = "🎉 You completed all today's goals! 🏆"

# --- Создание окна ---
root = Tk()
root.title("PROFILE")
root.configure(bg="#232323")
window_width = 390
window_height = 560

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.overrideredirect(True)

# --- Верхняя панель ---
title_bar = Frame(root, bg="#232323")
title_bar.pack(side=TOP, fill=X)
Label(title_bar, text="FitVision", fg="white", bg="#232323", font=("Verdana", 9, "bold")).pack(side=LEFT, padx=10)
Button(title_bar, text="✕", fg="white", bg="#232323", font=("Verdana", 9, "bold"),
       command=root.destroy, borderwidth=0).pack(side=RIGHT, padx=5, pady=2)

# --- Имя пользователя ---
Label(root, text=username, fg="white", bg="#232323", font=("Verdana", 16, "bold")).pack(pady=20)

# --- Блок информации ---
info_frame = Frame(root, bg="#121212")
info_frame.pack(pady=10)

# --- Прогресс ---
Label(root, text="Today Activities", fg="white", bg="#232323", font=("Verdana", 12, "bold")).pack(pady=(20, 5))

progress_frame = Frame(root, bg="#232323")
progress_frame.pack(pady=10)

# ✅ Отображаем текст активности
Label(progress_frame, text=activity_text, fg="white", bg="#232323",
      font=("Verdana", 11, "bold"), wraplength=300, justify="center").pack()

# --- Навигация ---
nav_frame = Frame(root, bg="#232323")
nav_frame.pack(pady=20)

def open_home():
    root.destroy()
    subprocess.Popen([".venv\\Scripts\\python", "home.py"], shell=True)

def open_goals():
    top = Toplevel(root)
    top.title("Achievements")
    top.configure(bg="#232323")
    window_width = 300
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    top.geometry(f"{window_width}x{window_height}+{x}+{y}")
    top.overrideredirect(True)

    title_bar = Frame(top, bg="#232323")
    title_bar.pack(side=TOP, fill=X)
    Label(title_bar, text="FitVision", fg="white", bg="#232323", font=("Verdana", 9, "bold")).pack(side=LEFT, padx=10)
    Button(title_bar, text="✕", fg="white", bg="#232323", font=("Verdana", 9, "bold"),
           command=top.destroy, borderwidth=0).pack(side=RIGHT, padx=5, pady=2)

    # 🎖 Показываем достижение
    Label(top, text="Achievements", fg="white", bg="#232323", font=("Verdana", 13, "bold")).pack(pady=20)
    if progress_percent >= 100:
        Label(top, text="🏅 You achieved today's goal!", fg="gold", bg="#232323", font=("Verdana", 12, "bold")).pack(pady=30)
    elif progress_percent >= 50:
        Label(top, text="⚡ Almost there! Keep pushing!", fg="yellow", bg="#232323", font=("Verdana", 12, "bold")).pack(pady=30)
    else:
        Label(top, text="❌ Not yet achieved. Try again!", fg="gray", bg="#232323", font=("Verdana", 12, "bold")).pack(pady=30)

def back():
    root.destroy()
    subprocess.Popen([".venv\\Scripts\\python", "dashboard.py"], shell=True)

Button(nav_frame, text="DAILY PLAN", width=20, bg="#232323", fg="white", border=0,
       font=("Verdana", 16, "bold"), command=open_home).pack(pady=5)

Button(nav_frame, text="GOALS REACHED", width=20, bg="#232323", fg="white", border=0,
       font=("Verdana", 16, "bold"), command=open_goals).pack(pady=5)

Button(root, text="back", bg="#232323", fg="white", border=0, command=back).place(x=13, y=50)

root.mainloop()
