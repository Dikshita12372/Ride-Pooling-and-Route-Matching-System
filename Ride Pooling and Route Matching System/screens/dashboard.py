import tkinter as tk

from screens.offer_ride import open_offer_ride
from screens.find_ride import open_find_ride
from screens.requests import open_my_requests
from screens.my_rides import open_my_rides

from DSA.stack import NavigationStack


def open_dashboard(user, on_logout=None):

    dashboard = tk.Toplevel()

    dashboard.title("Ride Pooling - Dashboard")
    dashboard.geometry("900x600")
    dashboard.configure(bg="#F3F6FF")
    dashboard.resizable(False, False)

    # ==========================================
    # STACK DSA
    # ==========================================
    #
    # The stack holds the actual chain of screens the user has
    # navigated through, each entry pairing a page name with its
    # window. "Back" pops the current screen off the stack and
    # re-shows whatever is now on top - real LIFO navigation,
    # not just a history log.

    navigation_stack = NavigationStack()

    # Dashboard is the first page
    navigation_stack.push({"name": "Dashboard", "window": dashboard})

    # ==========================================
    # GO BACK (pop the stack)
    # ==========================================

    def go_back():

        # Pop the screen we're leaving
        current_page = navigation_stack.pop()

        if current_page and current_page["window"] is not dashboard:
            current_page["window"].destroy()

        # Whatever is now on top of the stack is where we land
        previous_page = navigation_stack.peek()

        if previous_page:
            previous_page["window"].deiconify()

    # ==========================================
    # FUNCTION TO OPEN A PAGE
    # ==========================================

    def open_page(page_name, page_function):

        # Hide the dashboard while a sub-screen is open, so
        # "back" has something real to deiconify rather than
        # relying on it being left visible underneath
        dashboard.withdraw()

        # Open the selected page, handing it the go_back
        # callback so its own Back button pops the stack
        page_window = page_function(user, go_back)

        # Push the new screen onto the stack
        navigation_stack.push(
            {"name": page_name, "window": page_window}
        )

    # ==========================================
    # HEADER
    # ==========================================

    header = tk.Frame(
        dashboard,
        bg="#4F46E5",
        height=90
    )

    header.pack(fill="x")

    tk.Label(
        header,
        text="🚗 Ride Pooling System",
        font=("Arial", 22, "bold"),
        bg="#4F46E5",
        fg="white"
    ).pack(
        side="left",
        padx=30,
        pady=25
    )

    tk.Label(
        header,
        text=f"Welcome, {user['name']}!",
        font=("Arial", 12),
        bg="#4F46E5",
        fg="white"
    ).pack(
        side="right",
        padx=30
    )

    # ==========================================
    # MAIN AREA
    # ==========================================

    main_frame = tk.Frame(
        dashboard,
        bg="#F3F6FF"
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=35
    )

    tk.Label(
        main_frame,
        text="What would you like to do?",
        font=("Arial", 22, "bold"),
        bg="#F3F6FF",
        fg="#1F2937"
    ).pack(
        pady=(10, 30)
    )

    # ==========================================
    # CARDS
    # ==========================================

    cards_frame = tk.Frame(
        main_frame,
        bg="#F3F6FF"
    )

    cards_frame.pack()

    # ==========================================
    # OFFER RIDE CARD
    # ==========================================

    offer_card = tk.Frame(
        cards_frame,
        bg="white",
        width=300,
        height=220
    )

    offer_card.pack(
        side="left",
        padx=15
    )

    offer_card.pack_propagate(False)

    tk.Label(
        offer_card,
        text="🚗",
        font=("Arial", 40),
        bg="white"
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        offer_card,
        text="Offer a Ride",
        font=("Arial", 17, "bold"),
        bg="white",
        fg="#1F2937"
    ).pack()

    tk.Label(
        offer_card,
        text="Share your ride with other students",
        font=("Arial", 10),
        bg="white",
        fg="#6B7280"
    ).pack(
        pady=8
    )

    tk.Button(
        offer_card,
        text="OFFER RIDE",
        bg="#4F46E5",
        fg="white",
        activebackground="#4338CA",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        width=20,
        relief="flat",
        cursor="hand2",
        command=lambda: open_page(
            "Offer Ride",
            open_offer_ride
        )
    ).pack(
        pady=8
    )

    # ==========================================
    # FIND RIDE CARD
    # ==========================================

    find_card = tk.Frame(
        cards_frame,
        bg="white",
        width=300,
        height=220
    )

    find_card.pack(
        side="left",
        padx=15
    )

    find_card.pack_propagate(False)

    tk.Label(
        find_card,
        text="🔍",
        font=("Arial", 40),
        bg="white"
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        find_card,
        text="Find a Ride",
        font=("Arial", 17, "bold"),
        bg="white",
        fg="#1F2937"
    ).pack()

    tk.Label(
        find_card,
        text="Find a ride matching your route",
        font=("Arial", 10),
        bg="white",
        fg="#6B7280"
    ).pack(
        pady=8
    )

    tk.Button(
        find_card,
        text="FIND RIDE",
        bg="#10B981",
        fg="white",
        activebackground="#059669",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        width=20,
        relief="flat",
        cursor="hand2",
        command=lambda: open_page(
            "Find Ride",
            open_find_ride
        )
    ).pack(
        pady=8
    )

    # ==========================================
    # BOTTOM BUTTONS
    # ==========================================

    bottom = tk.Frame(
        main_frame,
        bg="#F3F6FF"
    )

    bottom.pack(
        pady=35
    )

    # ==========================================
    # MY REQUESTS
    # ==========================================

    tk.Button(
        bottom,
        text="My Requests",
        width=18,
        font=("Arial", 10, "bold"),
        bg="#F59E0B",
        fg="white",
        activebackground="#D97706",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=lambda: open_page(
            "My Requests",
            open_my_requests
        )
    ).pack(
        side="left",
        padx=10
    )

    # ==========================================
    # MY RIDES
    # ==========================================

    tk.Button(
        bottom,
        text="My Rides",
        width=18,
        font=("Arial", 10, "bold"),
        bg="#8B5CF6",
        fg="white",
        activebackground="#7C3AED",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=lambda: open_page(
            "My Rides",
            open_my_rides
        )
    ).pack(
        side="left",
        padx=10
    )

    # ==========================================
    # LOGOUT
    # ==========================================

    def logout():

        # Clear Stack before logout
        navigation_stack.clear()

        dashboard.destroy()

        # Hand control back to the login screen
        if on_logout:
            on_logout()

    tk.Button(
        bottom,
        text="Logout",
        width=18,
        font=("Arial", 10, "bold"),
        bg="#EF4444",
        fg="white",
        activebackground="#DC2626",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=logout
    ).pack(
        side="left",
        padx=10
    )

    return dashboard