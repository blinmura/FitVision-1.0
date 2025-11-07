from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import json
import os
import sys
import threading

def open_profile(ui, root):
    ui.destroy()
    root.destroy()
    import profile

def open_video(url, ui):
    def _open():
        webbrowser.open(url)
        # Через 700 мс возвращаем фокус на окно
        ui.after(700, lambda: (ui.deiconify(), ui.lift(), ui.focus_force()))
    threading.Thread(target=_open, daemon=True).start()

def exit_to():
    sys.exit()

# Получение имени пользователя
if os.path.exists("accounts.json"):
    with open("accounts.json", "r") as f:
        accounts = json.load(f)
    username = accounts.get("last_logged_in", "User")
else:
    username = "User"

# --- Создаём скрытый root ---
root = Tk()
root.title("FitVision hidden root")
root.geometry("1x1+0+0")  # невидимый root
root.update()

# --- Основное UI окно ---
ui = Toplevel(root)
ui.title("FITVISION DASHBOARD")

# Размеры окна
window_width = 390
window_height = 560

# Получаем размеры экрана
screen_width = ui.winfo_screenwidth()
screen_height = ui.winfo_screenheight()

# Центрирование
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
ui.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Цвет и стиль
ui.configure(bg="#232323")
ui.overrideredirect(True)

# Заголовок
title_bar = Frame(ui, bg="#232323")
title_bar.pack(side=TOP, fill=X)
Label(title_bar, text="FitVision", fg="white", bg="#232323", font=("Verdana", 9, "bold")).pack(side=LEFT, padx=10)
Button(title_bar, text="✕", fg="white", bg="#232323", font=("Verdana", 9, "bold"), command=lambda: (ui.destroy(), root.destroy()), borderwidth=0).pack(side=RIGHT, padx=5, pady=2)

# Приветствие
welcome = Label(ui, text=f"Hello, {username}", fg="white", bg="#232323", font=("Verdana", 14, "bold"))
welcome.pack(pady=10)
welcome.bind("<Button-1>", lambda e: open_profile(ui, root))  # переход к профилю

# Популярные тренировки
Label(ui, text="Popular Cardio", fg="white", bg="#232323", font=("Verdana", 12, "bold")).pack(anchor="w", padx=20)

popular_frame = Frame(ui, bg="#232323")
popular_frame.pack(pady=10)

def open_cardio(title, duration):
    top = Toplevel(ui)
    top.title(title)
    top.config(bg="#232323")

    # Размеры окна
    window_width = 300
    window_height = 200
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    top.geometry(f"{window_width}x{window_height}+{x}+{y}")
    top.overrideredirect(True)

    title_bar = Frame(top, bg="#232323")
    title_bar.pack(side=TOP, fill=X)
    Label(title_bar, text="FitVision", fg="white", bg="#232323", font=("Verdana", 9, "bold")).pack(side=LEFT, padx=10)
    Button(title_bar, text="✕", fg="white", bg="#232323", font=("Verdana", 9, "bold"), command=top.destroy, borderwidth=0).pack(side=RIGHT, padx=5, pady=2)

    frame = Frame(top, bg="#2b2b2b", bd=4, relief="ridge")
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    Label(top, text=title, font=("Verdana", 12, "bold"), bg="#232323", fg="white", border=0, pady=25).pack()
    Label(top, text=f"Duration: {duration}", font=("Verdana", 10), bg="#232323", fg="white").pack()
    Label(top, text="This workout boosts your cardio health!", wraplength=280, bg="#232323", fg="white").pack(pady=25)

Button(popular_frame, text="Fat-Blasting Cardio", width=18, height=4, bg="#2e2e2e", fg="white", relief=FLAT,
       command=lambda: open_cardio("Fat-Blasting Cardio", "10 minutes")).grid(row=0, column=0, padx=10)
Button(popular_frame, text="Cardio Power-Up", width=18, height=4, bg="#2e2e2e", fg="white", relief=FLAT,
       command=lambda: open_cardio("Cardio Power-Up", "30 minutes")).grid(row=0, column=1)

# Новые видео (YouTube интеграция)
Label(ui, text="New Videos", fg="white", bg="#232323", font=("Verdana", 12, "bold")).pack(anchor="w", padx=20, pady=(20, 5))

video_frame = Frame(ui, bg="#232323")
video_frame.pack(pady=10)

Button(video_frame, text="Home Fitness Blast\n20 min", width=36, height=3, bg="#2e2e2e", fg="white", relief=FLAT,
       command=lambda: open_video("https://www.youtube.com/watch?v=UItWltVZZmE", ui)).pack(pady=5)
Button(video_frame, text="Quick Interval Run\n15 min", width=36, height=3, bg="#2e2e2e", fg="white", relief=FLAT,
       command=lambda: open_video("https://www.youtube.com/watch?v=ml6cT4AZdqI", ui)).pack(pady=5)

# Отображаем главное окно
ui.lift()
ui.focus_force()

root.mainloop()
