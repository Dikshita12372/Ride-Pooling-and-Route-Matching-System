# ==========================================
# LINKED LIST DSA
# ==========================================

class Node:

    def __init__(self, location):
        self.location = location
        self.next = None


class RouteLinkedList:

    def __init__(self):
        self.head = None

    # Add a location at the end
    def append(self, location):

        new_node = Node(location)

        # If list is empty
        if self.head is None:
            self.head = new_node
            return

        # Go to the last node
        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    # Display all locations
    def get_route(self):

        route = []

        current = self.head

        while current is not None:
            route.append(current.location)
            current = current.next

        return route

    # Check whether a location exists
    def contains(self, location):

        current = self.head

        while current is not None:

            if current.location.lower() == location.lower():
                return True

            current = current.next

        return False

    # Find position of a location
    def find_position(self, location):

        current = self.head
        position = 0

        while current is not None:

            if current.location.lower() == location.lower():
                return position

            current = current.next
            position += 1

        return -1

    # Clear the linked list
    def clear(self):

        self.head = None