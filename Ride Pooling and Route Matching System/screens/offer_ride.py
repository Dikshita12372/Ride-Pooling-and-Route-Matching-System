import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database import get_db_connection
from DSA.linked_list import RouteLinkedList


def open_offer_ride(user, go_back=None):

    window = tk.Toplevel()

    window.title("Offer a Ride")
    window.geometry("600x760")
    window.configure(bg="#F3F6FF")
    window.resizable(False, False)

    # =========================
    # HEADER
    # =========================

    header = tk.Frame(
        window,
        bg="#4F46E5",
        height=100
    )

    header.pack(fill="x")

    # Fall back to a plain destroy if this screen is ever
    # opened without a navigation stack behind it
    back_command = go_back if go_back is not None else window.destroy

    tk.Button(
        header,
        text="← Back",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#4F46E5",
        activebackground="#E0E7FF",
        relief="flat",
        cursor="hand2",
        command=back_command
    ).place(
        x=20,
        y=35
    )

    tk.Label(
        header,
        text="🚗 Offer a Ride",
        font=("Arial", 24, "bold"),
        bg="#4F46E5",
        fg="white"
    ).pack(pady=30)

    # =========================
    # FORM CARD
    # =========================

    card = tk.Frame(
        window,
        bg="white",
        padx=40,
        pady=20
    )

    card.pack(
        padx=40,
        pady=20,
        fill="both"
    )

    # =========================
    # SOURCE
    # =========================

    tk.Label(
        card,
        text="Starting Location",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).pack(anchor="w")

    source_entry = tk.Entry(
        card,
        width=40,
        font=("Arial", 11)
    )

    source_entry.pack(
        pady=(5, 12)
    )

    # =========================
    # DESTINATION
    # =========================

    tk.Label(
        card,
        text="Destination",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).pack(anchor="w")

    destination_entry = tk.Entry(
        card,
        width=40,
        font=("Arial", 11)
    )

    destination_entry.pack(
        pady=(5, 12)
    )

    # =========================
    # ROUTE / STOPS
    # =========================

    tk.Label(
        card,
        text="Route / Intermediate Stops",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).pack(anchor="w")

    tk.Label(
        card,
        text="Example: Panvel → Kharghar → Vashi → Bandra → Goregaon",
        font=("Arial", 8),
        bg="white",
        fg="#6B7280"
    ).pack(anchor="w")

    route_entry = tk.Entry(
        card,
        width=40,
        font=("Arial", 11)
    )

    route_entry.pack(
        pady=(5, 12)
    )

    # =========================
    # DATE
    # =========================

    tk.Label(
        card,
        text="Ride Date (YYYY-MM-DD)",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).pack(anchor="w")

    date_entry = tk.Entry(
        card,
        width=40,
        font=("Arial", 11)
    )

    date_entry.pack(
        pady=(5, 12)
    )

    # =========================
    # TIME
    # =========================

    tk.Label(
        card,
        text="Ride Time (HH:MM)",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).pack(anchor="w")

    time_entry = tk.Entry(
        card,
        width=40,
        font=("Arial", 11)
    )

    time_entry.pack(
        pady=(5, 12)
    )

    # =========================
    # SEATS
    # =========================

    tk.Label(
        card,
        text="Available Seats",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).pack(anchor="w")

    seats_entry = tk.Entry(
        card,
        width=40,
        font=("Arial", 11)
    )

    seats_entry.pack(
        pady=(5, 12)
    )

    # =========================
    # PRICE
    # =========================

    tk.Label(
        card,
        text="Price per Passenger (₹)",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).pack(anchor="w")

    price_entry = tk.Entry(
        card,
        width=40,
        font=("Arial", 11)
    )

    price_entry.pack(
        pady=(5, 18)
    )

    # =========================
    # OFFER RIDE FUNCTION
    # =========================

    def offer_ride():

        source = source_entry.get().strip()

        destination = destination_entry.get().strip()

        route = route_entry.get().strip()
        route_list = RouteLinkedList()

        ride_date = date_entry.get().strip()

        ride_time = time_entry.get().strip()

        seats = seats_entry.get().strip()

        price = price_entry.get().strip()

        # =========================
        # BASIC VALIDATION
        # =========================

        if not source:

            messagebox.showerror(
                "Validation Error",
                "Please enter the starting location."
            )

            return

        if not destination:

            messagebox.showerror(
                "Validation Error",

                "Please enter the destination."
            )

            return

        if source.lower() == destination.lower():

            messagebox.showerror(
                "Validation Error",
                "Starting location and destination cannot be the same."
            )

            return

        # =========================
        # ROUTE VALIDATION
        # =========================

        if not route:

            messagebox.showerror(
                "Validation Error",
                "Please enter the complete route."
            )

            return

        # Split route using →
        route = route.replace("->", "→")

        locations = [
            location.strip()
            for location in route.split("→")
            if location.strip()
        ]

        # Need at least source + destination

        if len(locations) < 2:

            messagebox.showerror(
                "Validation Error",
                "Route must contain at least starting location and destination.\n\n"
                "Example:\n"
                "Panvel → Kharghar → Vashi → Goregaon"
            )

            return
        # =========================
        # LINKED LIST DSA
        # =========================

        duplicate_location = None

        for location in locations:

            # Use the linked list to check whether this stop
            # was already added earlier in the route
            if route_list.contains(location):
                duplicate_location = location
                break

            route_list.append(location)

        if duplicate_location:

            messagebox.showerror(
                "Validation Error",
                f"'{duplicate_location}' appears more than once "
                "in the route."
            )

            return

        # Get route back from the Linked List
        route = " → ".join(route_list.get_route())

        # Use the linked list to confirm the Destination is
        # genuinely the LAST stop in the route (by position,
        # not just string comparison)
        destination_position = route_list.find_position(destination)
        last_position = len(route_list.get_route()) - 1

        if destination_position == -1 or destination_position != last_position:

            messagebox.showerror(
                "Validation Error",
                "The route must end with the Destination."
            )

            return

        # =========================
        # DATE VALIDATION
        # =========================

        try:

            selected_date = datetime.strptime(
                ride_date,
                "%Y-%m-%d"
            ).date()

            if selected_date < datetime.now().date():

                messagebox.showerror(
                    "Validation Error",
                    "Ride date cannot be in the past."
                )

                return

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Date must be in YYYY-MM-DD format."
            )

            return

        # =========================
        # TIME VALIDATION
        # =========================

        try:

            datetime.strptime(
                ride_time,
                "%H:%M"
            )

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Time must be in HH:MM format."
            )

            return

        # =========================
        # SEATS VALIDATION
        # =========================

        try:

            seats = int(seats)

            if seats <= 0:

                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Seats must be a positive number."
            )

            return

        # =========================
        # PRICE VALIDATION
        # =========================

        try:

            price = float(price)

            if price < 0:

                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Please enter a valid price."
            )

            return

        # =========================
        # DATABASE
        # =========================

        try:

            db = get_db_connection()

            cursor = db.cursor()

            query = """
            INSERT INTO rides
            (
                driver_id,
                source,
                destination,
                ride_date,
                ride_time,
                total_seats,
                available_seats,
                price,
                route
            )

            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            """

            cursor.execute(
                query,
                (
                    user["user_id"],
                    source,
                    destination,
                    ride_date,
                    ride_time,
                    seats,
                    seats,
                    price,
                    route
                )
            )

            db.commit()

            cursor.close()

            db.close()

            # =========================
            # SUCCESS
            # =========================

            messagebox.showinfo(
                "Success",
                "Ride offered successfully!\n\n"
                "Your ride is now available."
            )

            # Leave through the same navigation path we came in
            # by, so the Stack stays in sync
            back_command()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not offer ride.\n\n{e}"
            )

    # =========================
    # OFFER BUTTON
    # =========================

    tk.Button(
        card,
        text="OFFER RIDE",
        font=("Arial", 11, "bold"),
        bg="#4F46E5",
        fg="white",
        width=30,
        height=2,
        relief="flat",
        cursor="hand2",
        command=offer_ride
    ).pack()

    # =========================
    # FOCUS
    # =========================

    source_entry.focus()

    return window