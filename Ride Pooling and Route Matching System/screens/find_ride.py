import tkinter as tk
from tkinter import messagebox

from database import get_db_connection
from DSA.tree import RouteTree
from DSA.array import RideArray



# ==========================================
# OPEN FIND RIDE
# ==========================================

def open_find_ride(user, go_back=None):

    window = tk.Toplevel()

    window.title("Find a Ride")

    window.geometry("950x700")

    window.configure(
        bg="#F3F6FF"
    )

    window.resizable(
        False,
        False
    )

    # ==========================================
    # ARRAY
    # ==========================================

    ride_array = RideArray()

    # ==========================================
    # HEADER
    # ==========================================

    header = tk.Frame(
        window,
        bg="#10B981",
        height=100
    )

    header.pack(
        fill="x"
    )

    # Back button

    # Fall back to a plain destroy if this screen is ever
    # opened without a navigation stack behind it
    back_command = go_back if go_back is not None else window.destroy

    tk.Button(
        header,
        text="← Back",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#10B981",
        activebackground="#D1FAE5",
        relief="flat",
        cursor="hand2",
        command=back_command
    ).place(
        x=20,
        y=35
    )

    tk.Label(
        header,
        text="🔍 Find a Ride",
        font=("Arial", 24, "bold"),
        bg="#10B981",
        fg="white"
    ).pack(
        pady=30
    )

    # ==========================================
    # SEARCH AREA
    # ==========================================

    search_frame = tk.Frame(
        window,
        bg="white",
        padx=20,
        pady=20
    )

    search_frame.pack(
        fill="x",
        padx=30,
        pady=20
    )

    # FROM

    tk.Label(
        search_frame,
        text="From",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=5
    )

    source_entry = tk.Entry(
        search_frame,
        width=25,
        font=("Arial", 11)
    )

    source_entry.grid(
        row=1,
        column=0,
        padx=10
    )

    # TO

    tk.Label(
        search_frame,
        text="To",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).grid(
        row=0,
        column=1,
        padx=10,
        pady=5
    )

    destination_entry = tk.Entry(
        search_frame,
        width=25,
        font=("Arial", 11)
    )

    destination_entry.grid(
        row=1,
        column=1,
        padx=10
    )

    # ==========================================
    # RESULTS AREA
    # ==========================================

    results_frame = tk.Frame(
        window,
        bg="#F3F6FF"
    )

    results_frame.pack(
        fill="both",
        expand=True,
        padx=30
    )

    # ==========================================
    # SHOW DETAILS
    # ==========================================

    def show_details(ride):

        details = tk.Toplevel(
            window
        )

        details.title(
            "Ride Details"
        )

        details.geometry(
            "550x600"
        )

        details.configure(
            bg="#F3F6FF"
        )

        # ======================================
        # HEADER
        # ======================================

        details_header = tk.Frame(
            details,
            bg="#4F46E5",
            height=80
        )

        details_header.pack(
            fill="x"
        )

        tk.Button(
            details_header,
            text="← Back",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#4F46E5",
            relief="flat",
            cursor="hand2",
            command=details.destroy
        ).place(
            x=15,
            y=25
        )

        tk.Label(
            details_header,
            text="🚗 Ride Details",
            font=("Arial", 20, "bold"),
            bg="#4F46E5",
            fg="white"
        ).pack(
            pady=23
        )

        # ======================================
        # CARD
        # ======================================

        card = tk.Frame(
            details,
            bg="white",
            padx=30,
            pady=25
        )

        card.pack(
            padx=30,
            pady=25,
            fill="both",
            expand=True
        )

        # ======================================
        # DATA
        # ======================================

        rating = float(
            ride["rating"] or 0
        )

        information = [

            (
                "Driver",
                ride["driver_name"]
            ),

            (
                "From",
                ride["source"]
            ),

            (
                "To",
                ride["destination"]
            ),

            (
                "Date",
                str(ride["ride_date"])
            ),

            (
                "Time",
                str(ride["ride_time"])
            ),

            (
                "Available Seats",
                str(ride["available_seats"])
            ),

            (
                "Price",
                f"₹{ride['price']}"
            ),

            (
                "Route",
                ride["route"]
            ),

            (
                "Rating",
                f"{rating:.1f} ⭐"
            )
        ]

        for label, value in information:

            row = tk.Frame(
                card,
                bg="white"
            )

            row.pack(
                fill="x",
                pady=6
            )

            tk.Label(
                row,
                text=f"{label}:",
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#374151",
                width=18,
                anchor="w"
            ).pack(
                side="left"
            )

            tk.Label(
                row,
                text=value,
                font=("Arial", 10),
                bg="white",
                fg="#4B5563",
                wraplength=300,
                justify="left"
            ).pack(
                side="left"
            )

        # ======================================
        # REQUEST / STATUS
        # ======================================

        current_status = ride.get(
            "request_status"
        )

        if current_status:

            status_text = (
                f"Status: {current_status}"
            )

            if current_status == "PENDING":

                status_bg = "#F59E0B"

            elif current_status == "ACCEPTED":

                status_bg = "#10B981"

            elif current_status == "REJECTED":

                status_bg = "#EF4444"

            else:

                status_bg = "#6B7280"

            tk.Label(
                card,
                text=status_text,
                font=("Arial", 11, "bold"),
                bg=status_bg,
                fg="white",
                padx=15,
                pady=8
            ).pack(
                pady=15
            )

        else:

            tk.Button(
                card,
                text="REQUEST THIS RIDE",
                font=("Arial", 10, "bold"),
                bg="#4F46E5",
                fg="white",
                width=25,
                height=2,
                relief="flat",
                cursor="hand2",
                command=lambda:
                    request_ride(
                        ride,
                        details
                    )
            ).pack(
                pady=20
            )

    # ==========================================
    # REQUEST RIDE
    # ==========================================

    def request_ride(
        ride,
        details_window=None
    ):

        # ======================================
        # OWN RIDE CHECK
        # ======================================

        if ride["driver_id"] == user["user_id"]:

            messagebox.showerror(
                "Not Allowed",
                "You cannot request your own ride."
            )

            return

        try:

            db = get_db_connection()

            cursor = db.cursor()

            # ==================================
            # CHECK EXISTING REQUEST
            # ==================================

            cursor.execute(
                """
                SELECT
                    request_id,
                    status

                FROM ride_requests

                WHERE ride_id = %s
                AND passenger_id = %s
                """,
                (
                    ride["ride_id"],
                    user["user_id"]
                )
            )

            existing = cursor.fetchone()

            if existing:

                messagebox.showwarning(
                    "Already Requested",
                    f"You have already requested this ride.\n\n"
                    f"Status: {existing[1]}"
                )

                cursor.close()

                db.close()

                return

            # ==================================
            # CHECK SEATS
            # ==================================

            if ride["available_seats"] <= 0:

                messagebox.showerror(
                    "Ride Full",
                    "No seats are available."
                )

                cursor.close()

                db.close()

                return

            # ==================================
            # INSERT REQUEST
            # ==================================

            cursor.execute(
                """
                INSERT INTO ride_requests
                (
                    ride_id,
                    passenger_id,
                    status
                )

                VALUES
                (
                    %s,
                    %s,
                    'PENDING'
                )
                """,
                (
                    ride["ride_id"],
                    user["user_id"]
                )
            )

            db.commit()

            cursor.close()

            db.close()

            # ==================================
            # UPDATE LOCAL STATUS
            # ==================================

            ride["request_status"] = "PENDING"

            messagebox.showinfo(
                "Request Sent",
                "Ride request sent successfully!\n\n"
                "Status: PENDING"
            )

            if details_window:

                details_window.destroy()

            # Refresh search results

            search_rides()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not request ride.\n\n{e}"
            )

    # ==========================================
    # DISPLAY RIDES
    # ==========================================

    def display_rides(rides):

        # Clear old results

        for widget in results_frame.winfo_children():

            widget.destroy()

        # ======================================
        # NO RESULTS
        # ======================================

        if not rides:

            tk.Label(
                results_frame,
                text="No matching rides found.",
                font=("Arial", 15, "bold"),
                bg="#F3F6FF",
                fg="#6B7280"
            ).pack(
                pady=50
            )

            return

        # ======================================
        # DISPLAY EACH RIDE
        # ======================================

        for ride in rides:

            card = tk.Frame(
                results_frame,
                bg="white",
                padx=20,
                pady=15
            )

            card.pack(
                fill="x",
                pady=8
            )

            # ==================================
            # DRIVER
            # ==================================

            tk.Label(
                card,
                text=f"👤 {ride['driver_name']}",
                font=("Arial", 14, "bold"),
                bg="white",
                fg="#1F2937"
            ).grid(
                row=0,
                column=0,
                sticky="w"
            )

            # ==================================
            # RATING
            # ==================================

            rating = float(
                ride["rating"] or 0
            )

            tk.Label(
                card,
                text=f"{rating:.1f} ⭐",
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#F59E0B"
            ).grid(
                row=0,
                column=1,
                padx=20
            )

            # ==================================
            # PRICE
            # ==================================

            tk.Label(
                card,
                text=f"₹{ride['price']}",
                font=("Arial", 14, "bold"),
                bg="white",
                fg="#10B981"
            ).grid(
                row=0,
                column=2,
                padx=20
            )

            # ==================================
            # ROUTE
            # ==================================

            tk.Label(
                card,
                text=(
                    f"{ride['source']}"
                    f"  →  "
                    f"{ride['destination']}"
                ),
                font=("Arial", 12, "bold"),
                bg="white",
                fg="#4F46E5"
            ).grid(
                row=1,
                column=0,
                columnspan=3,
                sticky="w",
                pady=8
            )

            # ==================================
            # DATE / TIME
            # ==================================

            tk.Label(
                card,
                text=(
                    f"📅 {ride['ride_date']}    "
                    f"🕐 {ride['ride_time']}"
                ),
                font=("Arial", 10),
                bg="white",
                fg="#4B5563"
            ).grid(
                row=2,
                column=0,
                sticky="w"
            )

            # ==================================
            # SEATS
            # ==================================

            tk.Label(
                card,
                text=(
                    f"🪑 "
                    f"{ride['available_seats']} seats"
                ),
                font=("Arial", 10),
                bg="white",
                fg="#4B5563"
            ).grid(
                row=2,
                column=1,
                padx=20
            )

            # ==================================
            # ROUTE
            # ==================================

            tk.Label(
                card,
                text=f"🛣 {ride['route']}",
                font=("Arial", 9),
                bg="white",
                fg="#6B7280",
                wraplength=500,
                justify="left"
            ).grid(
                row=3,
                column=0,
                columnspan=3,
                sticky="w",
                pady=5
            )

            # ==================================
            # REQUEST STATUS
            # ==================================

            status = ride.get(
                "request_status"
            )

            if status:

                if status == "PENDING":

                    status_bg = "#F59E0B"

                elif status == "ACCEPTED":

                    status_bg = "#10B981"

                elif status == "REJECTED":

                    status_bg = "#EF4444"

                else:

                    status_bg = "#6B7280"

                tk.Label(
                    card,
                    text=f"Status: {status}",
                    font=("Arial", 9, "bold"),
                    bg=status_bg,
                    fg="white",
                    padx=10,
                    pady=5
                ).grid(
                    row=4,
                    column=0,
                    sticky="w",
                    pady=8
                )

            # ==================================
            # DETAILS BUTTON
            # ==================================

            tk.Button(
                card,
                text="VIEW DETAILS",
                bg="#4F46E5",
                fg="white",
                font=("Arial", 9, "bold"),
                relief="flat",
                cursor="hand2",
                command=lambda r=ride:
                    show_details(r)
            ).grid(
                row=0,
                column=3,
                rowspan=5,
                padx=10
            )

    # ==========================================
    # SEARCH RIDES
    # ==========================================

    def search_rides():

        source = source_entry.get().strip()

        destination = (
            destination_entry.get().strip()
        )

        # ======================================
        # VALIDATION
        # ======================================

        if not source:

            messagebox.showerror(
                "Validation Error",
                "Please enter starting location."
            )

            source_entry.focus()

            return

        if not destination:

            messagebox.showerror(
                "Validation Error",
                "Please enter destination."
            )

            destination_entry.focus()

            return

        if source.lower() == destination.lower():

            messagebox.showerror(
                "Validation Error",
                "Starting location and destination "
                "cannot be the same."
            )

            return

        try:

            # ==================================
            # DATABASE
            # ==================================

            db = get_db_connection()

            cursor = db.cursor(
                dictionary=True
            )

            # ==================================
            # GET AVAILABLE RIDES
            # ==================================

            query = """
            SELECT

                r.ride_id,

                r.driver_id,

                r.source,

                r.destination,

                r.ride_date,

                r.ride_time,

                r.available_seats,

                r.price,

                r.route,

                u.name AS driver_name,

                COALESCE(
                    (
                        SELECT AVG(rt.rating)

                        FROM ratings rt

                        WHERE rt.driver_id = r.driver_id
                    ),
                    0
                ) AS rating,

                rr.status AS request_status

            FROM rides r

            JOIN users u
                ON r.driver_id = u.user_id

            LEFT JOIN ride_requests rr

                ON rr.ride_id = r.ride_id

                AND rr.passenger_id = %s

            WHERE r.status = 'AVAILABLE'

            AND r.available_seats > 0

            AND r.driver_id != %s

            ORDER BY
                r.ride_date,
                r.ride_time
            """

            cursor.execute(
                query,
                (
                    user["user_id"],
                    user["user_id"]
                )
            )

            database_rides = (
                cursor.fetchall()
            )

            cursor.close()

            db.close()

            # ==================================
            # TREE DSA
            # ==================================
            #
            # Build ONE tree out of every candidate ride's
            # route. Rides that share a route prefix share
            # nodes; where routes diverge, the tree branches.
            # Then a single DFS finds every ride that passes
            # through `source` before `destination`.

            route_tree = RouteTree()

            for ride in database_rides:

                route_text = ride["route"]

                # If route is empty, skip it

                if not route_text:

                    continue

                # Example:
                #
                # Panvel → Kharghar → Vashi → Goregaon

                locations = [
                    location.strip()

                    for location
                    in route_text.split("→")

                    if location.strip()
                ]

                route_tree.insert_route(
                    locations,
                    ride["ride_id"]
                )

            # ==================================
            # DFS TREE MATCH
            # ==================================

            matched_ride_ids = route_tree.find_matching_rides(
                source,
                destination
            )

            matched_rides = [
                ride
                for ride in database_rides
                if ride["ride_id"] in matched_ride_ids
            ]

            # ==================================
            # ARRAY DSA
            # ==================================

            ride_array.clear()

            for ride in matched_rides:

                ride_array.add(
                    ride
                )

            # ==================================
            # DISPLAY
            # ==================================

            display_rides(
                ride_array.get_all()
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not search rides.\n\n{e}"
            )

    # ==========================================
    # SEARCH BUTTON
    # ==========================================

    tk.Button(
        search_frame,
        text="SEARCH RIDES",
        bg="#10B981",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18,
        height=2,
        relief="flat",
        cursor="hand2",
        command=search_rides
    ).grid(
        row=1,
        column=2,
        padx=20
    )

    # ==========================================
    # INITIAL FOCUS
    # ==========================================

    source_entry.focus()

    return window