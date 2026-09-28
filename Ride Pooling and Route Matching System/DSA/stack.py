class NavigationStack:

    def __init__(self):
        self.stack = []

    # PUSH
    def push(self, page):
        self.stack.append(page)

    # POP
    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    # PEEK
    def peek(self):
        if self.stack:
            return self.stack[-1]
        return None

    # CHECK EMPTY
    def is_empty(self):
        return len(self.stack) == 0

    # CLEAR
    def clear(self):
        self.stack.clear()