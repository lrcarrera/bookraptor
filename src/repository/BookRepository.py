from src.model import Book


class BookRepository:
    __conn = None

    def __init__(self, conn):
        self.__conn = conn

    def persist(self, book: Book):
        self.__conn.autocommit = False
        cursor = self.__conn.cursor()
