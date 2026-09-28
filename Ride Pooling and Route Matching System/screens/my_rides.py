import tkinter as tk
from tkinter import messagebox
from database import get_db_connection
from DSA.queue import RequestQueue


# ==========================================
# MY RIDES
# ==========================================

def open_my_rides(user, go_back=None):

    window = tk.Toplevel()

    window.title("My Rides")
    window.geometry("950x700")
    window.configure(bg="#F3F6FF")
    window.resizable(False, False)

    request_queue = RequestQueue()

    # ==========================================
    # HEADER
    # ==========================================

    header = tk.Frame(
        window,
        bg="#8B5CF6",
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
        fg="#8B5CF6",
        activebackground="#E5E7EB",
        relief="flat",
        cursor="hand2",
        command=back_command
    ).place(
        x=20,
        y=35
    )

    tk.Label(
        header,
        text="🚗 My Rides",
        font=("Arial", 24, "bold"),
        bg="#8B5CF6",
        fg="white"
    ).pack(pady=30)

    # ==========================================
    # MAIN AREA
    # ==========================================

    main_frame = tk.Frame(
        window,
        bg="#F3F6FF"
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )

    # ==========================================
    # LOAD RIDES
    # ==========================================

    def load_rides():

        for widget in main_frame.winfo_children():
            widget.destroy()

        try:

            db = get_db_connection()

            cursor = db.cursor(dictionary=True)

            # Get rides offered by current user

            cursor.execute(
                """
                SELECT
                    ride_id,
                    source,
                    destination,
                    ride_date,
                    ride_time,
                    total_seats,
                    available_seats,
                    price,
                    route,
                    status

                FROM rides

                WHERE driver_id = %s

                ORDER BY ride_date, ride_time
                """,
                (user["user_id"],)
            )

            rides = cursor.fetchall()

            # ==================================
            # NO RIDES
            # ==================================

            if not rides:

                cursor.close()
                db.close()

                tk.Label(
                    main_frame,
                    text="You haven't offered any rides yet.",
                    font=("Arial", 16, "bold"),
                    bg="#F3F6FF",
                    fg="#6B7280"
                ).pack(pady=80)

                return

            # ==================================
            # DISPLAY EACH RIDE
            # ==================================

            for ride in rides:

                ride_card = tk.Frame(
                    main_frame,
                    bg="white",
                    padx=20,
                    pady=15
                )

                ride_card.pack(
                    fill="x",
                    pady=8
                )

                # Route

                tk.Label(
                    ride_card,
                    text=(
                        f"{ride['source']}  →  "
                        f"{ride['destination']}"
                    ),
                    font=("Arial", 15, "bold"),
                    bg="white",
                    fg="#4F46E5"
                ).pack(
                    anchor="w"
                )

                # Date / Time

                tk.Label(
                    ride_card,
                    text=(
                        f"📅 {ride['ride_date']}    "
                        f"🕐 {ride['ride_time']}"
                    ),
                    font=("Arial", 10),
                    bg="white",
                    fg="#4B5563"
                ).pack(
                    anchor="w",
                    pady=5
                )

                # Seats / Price

                tk.Label(
                    ride_card,
                    text=(
                        f"🪑 Available seats: "
                        f"{ride['available_seats']} / "
                        f"{ride['total_seats']}     "
                        f"💰 ₹{ride['price']}"
                    ),
                    font=("Arial", 10, "bold"),
                    bg="white",
                    fg="#10B981"
                ).pack(
                    anchor="w"
                )

                # Route

                tk.Label(
                    ride_card,
                    text=f"🛣 Route: {ride['route']}",
                    font=("Arial", 10),
                    bg="white",
                    fg="#4B5563",
                    wraplength=700
                ).pack(
                    anchor="w",
                    pady=5
                )

                # ==================================
                # REQUESTS FOR THIS RIDE
                # ==================================

                cursor.execute(
                    """
                    SELECT
                        rr.request_id,
                        rr.ride_id,
                        rr.passenger_id,
                        rr.status,
                        rr.requested_at,
                        u.name AS passenger_name,
                        u.email AS passenger_email,
                        u.phone AS passenger_phone

                    FROM ride_requests rr

                    JOIN users u
                        ON rr.passenger_id = u.user_id

                    WHERE rr.ride_id = %s

                    ORDER BY rr.requested_at ASC
                    """,
                    (ride["ride_id"],)
                )

                requests = cursor.fetchall()

                # Put pending requests into Queue, oldest first
                # (requests were already fetched ORDER BY
                # requested_at ASC, so enqueue order = arrival order)

                request_queue.clear()

                for request in requests:

                    if request["status"] == "PENDING":
                        request_queue.enqueue(request)

                # The ONLY request that can be actioned right now
                # is the one at the front of the queue - everyone
                # else has to wait their turn
                pending_in_queue = request_queue.get_all()

                next_actionable_id = (
                    pending_in_queue[0]["request_id"]
                    if pending_in_queue
                    else None
                )

                # ==================================
                # REQUEST SECTION
                # ==================================

                if requests:

                    tk.Label(
                        ride_card,
                        text="Ride Requests",
                        font=("Arial", 12, "bold"),
                        bg="white",
                        fg="#1F2937"
                    ).pack(
                        anchor="w",
                        pady=(15, 8)
                    )

                    for request in requests:

                        request_frame = tk.Frame(
                            ride_card,
                            bg="#F9FAFB",
                            padx=12,
                            pady=10
                        )

                        request_frame.pack(
                            fill="x",
                            pady=4
                        )

                        # Passenger information

                        tk.Label(
                            request_frame,
                            text=(
                                f"👤 {request['passenger_name']}"
                            ),
                            font=("Arial", 11, "bold"),
                            bg="#F9FAFB",
                            fg="#374151"
                        ).pack(
                            side="left"
                        )

                        tk.Label(
                            request_frame,
                            text=(
                                f"📞 {request['passenger_phone']}"
                            ),
                            font=("Arial", 9),
                            bg="#F9FAFB",
                            fg="#6B7280"
                        ).pack(
                            side="left",
                            padx=15
                        )

                        # Status

                        status_label = tk.Label(
                            request_frame,
                            text=request["status"],
                            font=("Arial", 9, "bold"),
                            padx=8,
                            pady=4
                        )

                        status_label.pack(
                            side="right",
                            padx=5
                        )

                        if request["status"] == "PENDING":

                            status_label.configure(
                                bg="#F59E0B",
                                fg="white"
                            )

                            # =========================
                            # QUEUE DSA
                            # =========================
                            # Only the request at the FRONT of
                            # the queue (the oldest pending one)
                            # can be actioned. Everyone else has
                            # to wait their turn - this is what
                            # actually enforces FIFO ordering.

                            if request["request_id"] == next_actionable_id:

                                # Accept

                                tk.Button(
                                    request_frame,
                                    text="ACCEPT",
                                    font=("Arial", 9, "bold"),
                                    bg="#10B981",
                                    fg="white",
                                    relief="flat",
                                    cursor="hand2",
                                    command=lambda r=request,
                                    ri=ride: accept_request(r, ri)
                                ).pack(
                                    side="right",
                                    padx=3
                                )

                                # Reject

                                tk.Button(
                                    request_frame,
                                    text="REJECT",
                                    font=("Arial", 9, "bold"),
                                    bg="#EF4444",
                                    fg="white",
                                    relief="flat",
                                    cursor="hand2",
                                    command=lambda r=request,
                                    ri=ride: reject_request(r, ri)
                                ).pack(
                                    side="right",
                                    padx=3
                                )

                            else:

                                # Find this request's position in
                                # the queue so the driver knows how
                                # long the wait is
                                queue_position = next(
                                    (
                                        index
                                        for index, queued in enumerate(pending_in_queue)
                                        if queued["request_id"] == request["request_id"]
                                    ),
                                    None
                                )

                                wait_text = (
                                    f"⏳ Waiting (#{queue_position + 1} in queue)"
                                    if queue_position is not None
                                    else "⏳ Waiting"
                                )

                                tk.Label(
                                    request_frame,
                                    text=wait_text,
                                    font=("Arial", 9, "italic"),
                                    bg="#F9FAFB",
                                    fg="#9CA3AF"
                                ).pack(
                                    side="right",
                                    padx=3
                                )

                        elif request["status"] == "ACCEPTED":

                            status_label.configure(
                                bg="#10B981",
                                fg="white"
                            )

                        elif request["status"] == "REJECTED":

                            status_label.configure(
                                bg="#EF4444",
                                fg="white"
                            )

                else:

                    tk.Label(
                        ride_card,
                        text="No requests for this ride yet.",
                        font=("Arial", 9),
                        bg="white",
                        fg="#9CA3AF"
                    ).pack(
                        anchor="w",
                        pady=(12, 0)
                    )

            cursor.close()
            db.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load rides.\n\n{e}"
            )

    # ==========================================
    # ACCEPT REQUEST
    # ==========================================

    def accept_request(request, ride):

        try:

            db = get_db_connection()

            cursor = db.cursor()

            # Check available seats

            cursor.execute(
                """
                SELECT available_seats
                FROM rides
                WHERE ride_id = %s
                """,
                (ride["ride_id"],)
            )

            result = cursor.fetchone()

            if not result or result[0] <= 0:

                messagebox.showerror(
                    "Ride Full",
                    "There are no available seats."
                )

                cursor.close()
                db.close()

                return

            # Accept request

            cursor.execute(
                """
                UPDATE ride_requests
                SET status = 'ACCEPTED'
                WHERE request_id = %s
                """,
                (request["request_id"],)
            )

            # Reduce available seat

            cursor.execute(
                """
                UPDATE rides
                SET available_seats = available_seats - 1
                WHERE ride_id = %s
                AND available_seats > 0
                """,
                (ride["ride_id"],)
            )

            # Check remaining seats
            cursor.execute(
                """
                SELECT available_seats
                FROM rides
                WHERE ride_id = %s
                """,
                (ride["ride_id"],)
            )

            remaining_seats = cursor.fetchone()[0]

# Mark ride FULL when no seats remain
            if remaining_seats == 0:
                cursor.execute(
                    """
                    UPDATE rides
                    SET status = 'FULL'
                    WHERE ride_id = %s
                    """,
                    (ride["ride_id"],)
            )
            db.commit()

            cursor.close()
            db.close()

            messagebox.showinfo(
                "Request Accepted",
                "Ride request accepted successfully!"
            )

            # Refresh page

            load_rides()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not accept request.\n\n{e}"
            )

    # ==========================================
    # REJECT REQUEST
    # ==========================================

    def reject_request(request, ride):

        try:

            db = get_db_connection()

            cursor = db.cursor()

            cursor.execute(
                """
                UPDATE ride_requests
                SET status = 'REJECTED'
                WHERE request_id = %s
                """,
                (request["request_id"],)
            )

            db.commit()

            cursor.close()
            db.close()

            messagebox.showinfo(
                "Request Rejected",
                "Ride request rejected."
            )

            # Refresh page

            load_rides()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not reject request.\n\n{e}"
            )

    # ==========================================
    # REFRESH BUTTON
    # ==========================================

    tk.Button(
        window,
        text="🔄 Refresh",
        font=("Arial", 10, "bold"),
        bg="#4F46E5",
        fg="white",
        activebackground="#4338CA",
        activeforeground="white",
        width=18,
        height=2,
        relief="flat",
        cursor="hand2",
        command=load_rides
    ).pack(
        pady=(0, 20)
    )

    # Initial load

    load_rides()

    return window