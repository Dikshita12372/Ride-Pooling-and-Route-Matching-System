class RideArray:

    def __init__(self):
        self.rides = []

    def add(self, ride):
        self.rides.append(ride)

    def get_all(self):
        return self.rides

    def clear(self):
        self.rides.clear()