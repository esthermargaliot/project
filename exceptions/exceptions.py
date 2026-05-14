class BookAlreadyExistsException(Exception):
    def __init__(self, title):
        super().__init__(f"Book '{title}' already exists.")

class MissingTitleException(Exception):
    def __init__(self):
        super().__init__("Field 'title' is required.")

class BookNotFoundException(Exception):
    def __init__(self, book_id):
        super().__init__(f"Book with id {book_id} not found.")