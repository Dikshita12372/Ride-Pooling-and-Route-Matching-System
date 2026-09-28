# ==========================================
# QUEUE DSA
# ==========================================

class RequestQueue:

    def __init__(self):
        self.queue = []

    # Add request to the rear
    def enqueue(self, request):
        self.queue.append(request)

    # Remove request from the front
    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)

        return None

    # View all requests
    def get_all(self):
        return self.queue

    # Check if queue is empty
    def is_empty(self):
        return len(self.queue) == 0

    # Get queue size
    def size(self):
        return len(self.queue)

    # Clear queue
    def clear(self):
        self.queue.clear()