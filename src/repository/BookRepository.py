from src.model import Book


class BookRepository:
    __conn = None

    def __init__(self, conn):
        self.__conn = conn
        #TODO: Lluis, Add connection to elastic parameters

    def persist(self, book: Book):
        #TODO: Lluis, create persist to Elastic method
        cursor = self.__conn.cursor()#remove line

