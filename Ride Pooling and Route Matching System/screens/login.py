import tkinter as tk
from tkinter import messagebox
from database import get_db_connection
from screens.dashboard import open_dashboard
import re


def login_user():

    email = email_entry.get().strip()
    password = password_entry.get()

    # =========================
    # VALIDATION
    # =========================

    if not email:
        messagebox.showerror(
            "Validation Error",
            "Please enter your email."
        )
        return

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.fullmatch(email_pattern, email):
        messagebox.showerror(
            "Validation Error",
            "Please enter a valid email address."
        )
        return

    if not password:
        messagebox.showerror(
            "Validation Error",
            "Please enter your password."
        )
        return

    # =========================
    # DATABASE
    # =========================

    try:

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        query = """
        SELECT user_id, name, email, role, phone
        FROM users
        WHERE email = %s AND password = %s
        """

        cursor.execute(query, (email, password))

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:

            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {user['name']}!"
            )
            root.withdraw()  # Hide the login window
            open_dashboard(
                user,
                on_logout=return_to_login
            )  # Open the dashboard window

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid email or password."
            )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Could not connect to database.\n\n{e}"
        )


# =========================
# RETURN TO LOGIN (after logout)
# =========================

def return_to_login():

    # Clear old credentials so the next person doesn't see them
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    root.deiconify()  # Bring the login window back
    email_entry.focus()


# =========================
# WINDOW
# =========================

root = tk.Tk()

root.title("Ride Pooling - Login")
root.geometry("500x600")
root.resizable(False, False)

root.configure(bg="#F3F6FF")


# =========================
# HEADER
# =========================

header = tk.Frame(
    root,
    bg="#4F46E5",
    height=140
)

header.pack(fill="x")


tk.Label(
    header,
    text="🚗 Ride Pooling",
    font=("Arial", 26, "bold"),
    bg="#4F46E5",
    fg="white"
).pack(pady=(30, 5))


tk.Label(
    header,
    text="Route Matching System",
    font=("Arial", 13),
    bg="#4F46E5",
    fg="#E0E7FF"
).pack()


# =========================
# LOGIN CARD
# =========================

card = tk.Frame(
    root,
    bg="white",
    padx=40,
    pady=35
)

card.pack(
    padx=45,
    pady=30,
    fill="both"
)


tk.Label(
    card,
    text="Welcome Back!",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#1F2937"
).pack(pady=(0, 25))


# =========================
# EMAIL
# =========================

tk.Label(
    card,
    text="Email",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#374151"
).pack(anchor="w")


email_entry = tk.Entry(
    card,
    width=38,
    font=("Arial", 11),
    relief="solid",
    bd=1
)

email_entry.pack(pady=(5, 18))


# =========================
# PASSWORD
# =========================

tk.Label(
    card,
    text="Password",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#374151"
).pack(anchor="w")


password_entry = tk.Entry(
    card,
    width=38,
    font=("Arial", 11),
    show="*",
    relief="solid",
    bd=1
)

password_entry.pack(pady=(5, 25))


# =========================
# LOGIN BUTTON
# =========================

tk.Button(
    card,
    text="LOGIN",
    font=("Arial", 11, "bold"),
    bg="#4F46E5",
    fg="white",
    activebackground="#4338CA",
    activeforeground="white",
    width=30,
    height=2,
    relief="flat",
    cursor="hand2",
    command=login_user
).pack()


# =========================
# FOOTER
# =========================

tk.Label(
    root,
    text="Ride together • Travel smarter",
    font=("Arial", 10),
    bg="#F3F6FF",
    fg="#6B7280"
).pack()


root.mainloop()