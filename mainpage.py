from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageChops
from tkinter import messagebox
import json
import os


def apply_gradient_mask(image):
    width, height = image.size
    mask = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(mask)
    for y in range(height):
        opacity = int(255 * (1 - y / height))
        draw.line((0, y, width, y), fill=opacity)
    background = Image.new("RGB", (width, height), "#232323")
    faded_image = ImageChops.composite(image, background, mask)
    return faded_image


# Работа с файлом аккаунтов
ACCOUNTS_FILE = "accounts.json"
def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        return {"users": {}, "last_logged_in": ""}
    with open(ACCOUNTS_FILE, "r") as f:
        return json.load(f)

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)



def open_new_window():
    root.destroy()
    import dashboard


def open_signup():
    signup_window = Toplevel(root)
    signup_window.title("BUILDING...")
    signup_window.configure(bg="#232323")
    signup_window.geometry("360x400")
    signup_window.resizable(False, False)
    signup_window.overrideredirect(True)

    signup_window.update_idletasks()
    width = signup_window.winfo_width()
    height = signup_window.winfo_height()
    x = (signup_window.winfo_screenwidth() // 2) - (width // 2)
    y = (signup_window.winfo_screenheight() // 2) - (height // 2)
    signup_window.geometry(f"{width}x{height}+{x}+{y}")

    title_bar = Frame(signup_window, bg="#232323")
    title_bar.pack(side=TOP, fill=X)
    Label(title_bar, text="TAKE ACTION", fg="white", bg="#232323", font=("Verdana", 9, "bold")).pack(side=LEFT, padx=10)
    Button(title_bar, text="✕", fg="white", bg="#232323", font=("Verdana", 9, "bold"), command=signup_window.destroy,
           borderwidth=0).pack(side=RIGHT, padx=5, pady=2)


    Label(signup_window, text="BUILD YOURSELF", fg="white", bg="#232323", font=("Verdana", 14, "bold")).pack(pady=20)

    Label(signup_window, text="Username", fg="gray", bg="#232323", font=("Verdana", 9)).pack(anchor="w", padx=40, pady=(10, 0))
    username_entry = Entry(signup_window, font=("Verdana", 10), bg="#2e2e2e", fg="white", insertbackground="white", relief=FLAT)
    username_entry.pack(padx=40, pady=5, fill=X)

    Label(signup_window, text="Password", fg="gray", bg="#232323", font=("Verdana", 9)).pack(anchor="w", padx=40, pady=(10, 0))
    password_entry = Entry(signup_window, show="*", font=("Verdana", 10), bg="#2e2e2e", fg="white", insertbackground="white", relief=FLAT)
    password_entry.pack(padx=40, pady=5, fill=X)

    Label(signup_window, text="Confirm Password", fg="gray", bg="#232323", font=("Verdana", 9)).pack(anchor="w", padx=40, pady=(10, 0))
    confirm_entry = Entry(signup_window, show="*", font=("Verdana", 10), bg="#2e2e2e", fg="white", insertbackground="white", relief=FLAT)
    confirm_entry.pack(padx=40, pady=5, fill=X)

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        confirm = confirm_entry.get()

        if not username or not password:
            messagebox.showwarning("Error", "Fill in all fields.")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        accounts = load_accounts()
        if username in accounts:
            messagebox.showerror("Error", "Username already exists.")
            return

        accounts[username] = password
        accounts["last_logged_in"] = username
        save_accounts(accounts)
        messagebox.showinfo("Success", f"Account '{username}' registered!")
        signup_window.destroy()

    Button(signup_window, text="BUILD IT", command=register_user,
           font=("Verdana", 10, "bold"), fg="white", bg="#232323",
           activebackground="#3a3a3a", bd=0, padx=10, pady=8, relief=FLAT).pack(pady=20)


def open_login():
    login_window = Toplevel(root)
    login_window.title("TAKE ACTION")
    login_window.geometry("360x300")
    login_window.resizable(False, False)
    login_window.configure(bg="#232323")
    login_window.overrideredirect(True)

    login_window.update_idletasks()
    width = login_window.winfo_width()
    height = login_window.winfo_height()
    x = (login_window.winfo_screenwidth() // 2) - (width // 2)
    y = (login_window.winfo_screenheight() // 2) - (height // 2)
    login_window.geometry(f"{width}x{height}+{x}+{y}")

    title_bar = Frame(login_window, bg="#232323")
    title_bar.pack(side=TOP, fill=X)
    Label(title_bar, text="TAKE ACTION", fg="white", bg="#232323", font=("Verdana", 9, "bold")).pack(side=LEFT, padx=10)
    Button(title_bar, text="✕", fg="white", bg="#232323", font=("Verdana", 9, "bold"), command=login_window.destroy,
           borderwidth=0).pack(side=RIGHT, padx=5, pady=2)

    Label(login_window, text="GO INTO ACTION", fg="white", bg="#232323", font=("Verdana", 14, "bold")).pack(pady=20)

    Label(login_window, text="Username", fg="gray", bg="#232323", font=("Verdana", 9)).pack(anchor="w", padx=40)
    username_entry = Entry(login_window, font=("Verdana", 10), bg="#2e2e2e", fg="white", insertbackground="white", relief=FLAT)
    username_entry.pack(padx=40, pady=5, fill=X)

    Label(login_window, text="Password", fg="gray", bg="#232323", font=("Verdana", 9)).pack(anchor="w", padx=40)
    password_entry = Entry(login_window, show="*", font=("Verdana", 10), bg="#2e2e2e", fg="white", insertbackground="white", relief=FLAT)
    password_entry.pack(padx=40, pady=5, fill=X)

    def login_user():
        username = username_entry.get()
        password = password_entry.get()
        accounts = load_accounts()

        if username in accounts and username != "last_logged_in" and accounts[username] == password:
            accounts["last_logged_in"] = username
            save_accounts(accounts)
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            login_window.destroy()
            open_new_window()
        else:
            messagebox.showerror("Error", "Invalid username or password.")


    Button(login_window, text="ACT", command=login_user,
           font=("Verdana", 10, "bold"), fg="white", bg="#232323",
           activebackground="#3a3a3a", bd=0, padx=10, pady=8, relief=FLAT).pack(pady=20)


# Главное окно
root = Tk()
root.title("FitVision")
window_width = 390
window_height = 860
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.configure(bg="#232323")
root.overrideredirect(True)

# Титульная панель
title_bar = Frame(root, bg="#232323")
title_bar.pack(side=TOP, fill=X)
Label(title_bar, text="FitVision", fg="white", bg="#232323", font=("Verdana", 9, "bold")).pack(side=LEFT, padx=10)
Button(title_bar, text="✕", fg="white", bg="#232323", font=("Verdana", 9, "bold"), command=root.destroy, borderwidth=0).pack(side=RIGHT, padx=5, pady=2)

# Изображение
img = Image.open("greek.jpg").resize((396, 550), Image.LANCZOS)
img = apply_gradient_mask(img)
photo = ImageTk.PhotoImage(img)
Label(root, image=photo, bg="#232323").pack(pady=10)

# Текст
Label(root, text="DISCIPLINE", font=("Verdana", 14, "bold"), fg="white", bg="#232323").pack()
Label(root, text="CONSISTENCY", font=("Verdana", 14, "bold"), fg="white", bg="#232323").pack()
Label(root, text="There is no instant way to a healthy life", font=("Verdana", 10), fg="gray", bg="#232323").pack(pady=5)

# Кнопка действия
Button(root, text="TAKE ACTION", font=("Verdana", 10, "bold"), fg="white", bg="#232323", padx=20, pady=19, border=0).pack(pady=10)

# Панель регистрации и логина
bottom_frame = Frame(root, bg="#232323")
bottom_frame.pack(side=BOTTOM, pady=10)
Label(bottom_frame, text="ALREADY HAVE AN ACCOUNT?", font=("Verdana", 10), fg="gray", bg="#232323").pack(side=LEFT)
Button(bottom_frame, text="LOGIN", font=("Verdana", 10, "bold"), fg="white", bg="#232323", border=0, command=open_login).pack(side=LEFT, padx=5)
Button(bottom_frame, text="REGISTER", font=("Verdana", 10, "bold"), fg="white", bg="#232323", border=0, command=open_signup).pack(side=LEFT)

root.mainloop()
