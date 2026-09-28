import tkinter as tk
from tkinter import messagebox
from database import get_db_connection
import re
import subprocess
import sys
import os


# ==========================================
# REGISTER USER
# ==========================================

def register_user():

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get()
    phone = phone_entry.get().strip()

    # ==========================================
    # NAME VALIDATION
    # ==========================================

    if not name:
        messagebox.showerror(
            "Validation Error",
            "Please enter your name."
        )
        return

    if not re.fullmatch(r"[A-Za-z ]+", name):
        messagebox.showerror(
            "Validation Error",
            "Name should contain only letters."
        )
        return

    # ==========================================
    # EMAIL VALIDATION
    # ==========================================

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

    # ==========================================
    # PASSWORD VALIDATION
    # ==========================================

    if not password:
        messagebox.showerror(
            "Validation Error",
            "Please enter a password."
        )
        return

    if len(password) < 6:
        messagebox.showerror(
            "Validation Error",
            "Password must contain at least 6 characters."
        )
        return

    # ==========================================
    # PHONE VALIDATION
    # ==========================================

    if not phone:
        messagebox.showerror(
            "Validation Error",
            "Please enter your phone number."
        )
        return

    if not phone.isdigit():
        messagebox.showerror(
            "Validation Error",
            "Phone number should contain only digits."
        )
        return

    if len(phone) != 10:
        messagebox.showerror(
            "Validation Error",
            "Phone number must contain exactly 10 digits."
        )
        return

    if phone[0] not in "6789":
        messagebox.showerror(
            "Validation Error",
            "Please enter a valid Indian mobile number."
        )
        return

    # ==========================================
    # DATABASE
    # ==========================================

    try:

        db = get_db_connection()
        cursor = db.cursor()

        # Check whether email already exists
        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            messagebox.showerror(
                "Registration Error",
                "An account with this email already exists."
            )

            cursor.close()
            db.close()

            return

        # Insert user
        query = """
        INSERT INTO users
        (
            name,
            email,
            password,
            phone
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """

        cursor.execute(
            query,
            (
                name,
                email,
                password,
                phone
            )
        )

        db.commit()

        cursor.close()
        db.close()

        messagebox.showinfo(
            "Registration Successful",
            "Your account has been created successfully! \n\nPlease login to continue."
        )

        root.destroy()  # Close the registration window
        subprocess.Popen(
    [sys.executable, "-m", "screens.login"],
    cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Could not create account.\n\n{e}"
        )


# ==========================================
# CLEAR FIELDS
# ==========================================

def clear_fields():

    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title("Ride Pooling - Register")

root.geometry("520x680")

root.resizable(False, False)

root.configure(
    bg="#F3F6FF"
)


# ==========================================
# HEADER
# ==========================================

header = tk.Frame(
    root,
    bg="#4F46E5",
    height=130
)

header.pack(
    fill="x"
)


tk.Label(
    header,
    text="🚗 Ride Pooling",
    font=("Arial", 26, "bold"),
    bg="#4F46E5",
    fg="white"
).pack(
    pady=(25, 5)
)


tk.Label(
    header,
    text="Route Matching System",
    font=("Arial", 13),
    bg="#4F46E5",
    fg="#E0E7FF"
).pack()


# ==========================================
# FORM CARD
# ==========================================

card = tk.Frame(
    root,
    bg="white",
    padx=35,
    pady=25
)

card.pack(
    padx=40,
    pady=25,
    fill="both"
)


tk.Label(
    card,
    text="Create Account",
    font=("Arial", 19, "bold"),
    bg="white",
    fg="#1F2937"
).pack(
    pady=(0, 20)
)


# ==========================================
# NAME
# ==========================================

tk.Label(
    card,
    text="Full Name",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#374151"
).pack(
    anchor="w"
)


name_entry = tk.Entry(
    card,
    font=("Arial", 11),
    width=38,
    relief="solid",
    bd=1
)

name_entry.pack(
    pady=(5, 12)
)


# ==========================================
# EMAIL
# ==========================================

tk.Label(
    card,
    text="Email",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#374151"
).pack(
    anchor="w"
)


email_entry = tk.Entry(
    card,
    font=("Arial", 11),
    width=38,
    relief="solid",
    bd=1
)

email_entry.pack(
    pady=(5, 12)
)


# ==========================================
# PASSWORD
# ==========================================

tk.Label(
    card,
    text="Password",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#374151"
).pack(
    anchor="w"
)


password_entry = tk.Entry(
    card,
    font=("Arial", 11),
    width=38,
    show="*",
    relief="solid",
    bd=1
)

password_entry.pack(
    pady=(5, 12)
)


# ==========================================
# PHONE
# ==========================================

tk.Label(
    card,
    text="Phone Number",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#374151"
).pack(
    anchor="w"
)


phone_entry = tk.Entry(
    card,
    font=("Arial", 11),
    width=38,
    relief="solid",
    bd=1
)

phone_entry.pack(
    pady=(5, 18)
)


# ==========================================
# REGISTER BUTTON
# ==========================================

tk.Button(
    card,
    text="CREATE ACCOUNT",
    font=("Arial", 11, "bold"),
    bg="#4F46E5",
    fg="white",
    activebackground="#4338CA",
    activeforeground="white",
    width=30,
    height=2,
    relief="flat",
    cursor="hand2",
    command=register_user
).pack(
    pady=(5, 10)
)


# ==========================================
# FOOTER
# ==========================================

tk.Label(
    root,
    text="Ride together • Travel smarter",
    font=("Arial", 10),
    bg="#F3F6FF",
    fg="#6B7280"
).pack()


# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()