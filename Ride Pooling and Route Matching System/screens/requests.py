import tkinter as tk
from tkinter import messagebox
from database import get_db_connection


def open_my_requests(user, go_back=None):

    window = tk.Toplevel()
    window.title("My Ride Requests")
    window.geometry("900x650")
    window.configure(bg="#F3F6FF")
    window.resizable(False, False)

    

    # =========================
# HEADER
# =========================

    header = tk.Frame(
        window,
        bg="#F59E0B",
        height=100
    )

    header.pack(fill="x")

# Back button
    # Fall back to a plain destroy if this screen is ever
    # opened without a navigation stack behind it
    back_command = go_back if go_back is not None else window.destroy

    tk.Button(
        header,
        text="← Back",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#F59E0B",
        activebackground="#FEF3C7",
        relief="flat",
        cursor="hand2",
        command=back_command
    ).place(
        x=20,
        y=35
    )   

    tk.Label(
        header,
        text="📋 My Ride Requests",
        font=("Arial", 24, "bold"),
        bg="#F59E0B",
        fg="white"
    ).pack(pady=30)

    # =========================
    # RESULTS AREA
    # =========================

    results_frame = tk.Frame(
        window,
        bg="#F3F6FF"
    )

    results_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=25
    )

    # =========================
    # STATUS COLOR
    # =========================

    def status_color(status):

        if status == "PENDING":
            return "#F59E0B"

        elif status == "ACCEPTED":
            return "#10B981"

        elif status == "REJECTED":
            return "#EF4444"

        elif status == "CANCELLED":
            return "#6B7280"

        return "#374151"

    # =========================
    # LOAD REQUESTS
    # =========================

    def load_requests():

        for widget in results_frame.winfo_children():
            widget.destroy()

        try:

            db = get_db_connection()

            cursor = db.cursor(dictionary=True)

            query = """
            SELECT
                rr.request_id,
                rr.status,
                rr.requested_at,

                r.ride_id,
                r.source,
                r.destination,
                r.ride_date,
                r.ride_time,
                r.price,
                r.route,
                r.available_seats,

                u.name AS driver_name

            FROM ride_requests rr

            JOIN rides r
                ON rr.ride_id = r.ride_id

            JOIN users u
                ON r.driver_id = u.user_id

            WHERE rr.passenger_id = %s

            ORDER BY rr.requested_at DESC
            """

            cursor.execute(
                query,
                (user["user_id"],)
            )

            requests = cursor.fetchall()

            cursor.close()
            db.close()

            # =========================
            # NO REQUESTS
            # =========================

            if not requests:

                tk.Label(
                    results_frame,
                    text="You haven't requested any rides yet.",
                    font=("Arial", 15, "bold"),
                    bg="#F3F6FF",
                    fg="#6B7280"
                ).pack(pady=80)

                return

            # =========================
            # DISPLAY REQUESTS
            # =========================

            for request in requests:

                card = tk.Frame(
                    results_frame,
                    bg="white",
                    padx=20,
                    pady=18
                )

                card.pack(
                    fill="x",
                    pady=8
                )

                # Route

                tk.Label(
                    card,
                    text=(
                        f"{request['source']}  →  "
                        f"{request['destination']}"
                    ),
                    font=("Arial", 15, "bold"),
                    bg="white",
                    fg="#4F46E5"
                ).pack(anchor="w")

                # Driver

                tk.Label(
                    card,
                    text=f"👤 Driver: {request['driver_name']}",
                    font=("Arial", 10),
                    bg="white",
                    fg="#374151"
                ).pack(anchor="w", pady=5)

                # Date / time

                tk.Label(
                    card,
                    text=(
                        f"📅 {request['ride_date']}    "
                        f"🕐 {request['ride_time']}"
                    ),
                    font=("Arial", 10),
                    bg="white",
                    fg="#4B5563"
                ).pack(anchor="w")

                # Price

                tk.Label(
                    card,
                    text=f"💰 Price: ₹{request['price']}",
                    font=("Arial", 10, "bold"),
                    bg="white",
                    fg="#10B981"
                ).pack(anchor="w", pady=5)

                # Route

                tk.Label(
                    card,
                    text=f"🛣 Route: {request['route']}",
                    font=("Arial", 10),
                    bg="white",
                    fg="#4B5563",
                    wraplength=650
                ).pack(anchor="w")

                # Status

                status_frame = tk.Frame(
                    card,
                    bg="white"
                )

                status_frame.pack(
                    fill="x",
                    pady=(12, 0)
                )

                tk.Label(
                    status_frame,
                    text="Status:",
                    font=("Arial", 11, "bold"),
                    bg="white",
                    fg="#374151"
                ).pack(side="left")

                tk.Label(
                    status_frame,
                    text=f" {request['status']} ",
                    font=("Arial", 10, "bold"),
                    bg=status_color(request["status"]),
                    fg="white",
                    padx=10,
                    pady=4
                ).pack(side="left", padx=8)

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load requests.\n\n{e}"
            )

    # =========================
    # REFRESH BUTTON
    # =========================

    tk.Button(
        window,
        text="🔄 Refresh Status",
        font=("Arial", 10, "bold"),
        bg="#4F46E5",
        fg="white",
        activebackground="#4338CA",
        activeforeground="white",
        width=20,
        height=2,
        relief="flat",
        cursor="hand2",
        command=load_requests
    ).pack(pady=(0, 20))

    # Load when opening
    load_requests()

    return window