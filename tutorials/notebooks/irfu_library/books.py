class Book:
    def __init__(self, name=None, author=None, isbn=None):

        if not isinstance(name, str):
            raise ValueError("`name` should be a string")

        if not isinstance(author, str):
            raise ValueError("`author` should be a string")

        if not isinstance(isbn, int):
            raise ValueError("`isbn` should be an integer")

        self.name = name
        self.author = author
        self.isbn = isbn

    def __repr__(self) -> str:
        return f""""{self.name}" by {self.author} [{self.isbn}]"""

    def order_from_amazon(self, copies = 1e99):
        raise NotImplementedError("Not written this code yet, and probably never should.")