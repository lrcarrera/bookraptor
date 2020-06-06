from typing import List

class Book:

    __book_id = None
    __book_title = None
    __author = None
    __description = None
    __publication_date = None
    __price = None
    __dynamic_content = {}

    def __init__(self, book_id):
        self.__book_id = book_id

    def get_book_id(self):
        return self.__book_id

    def set_book_id(self, book_id):
        self.__book_id = book_id

    def get_book_title(self):
        return self.__book_title

    def set_book_title(self, book_title):
        self.__book_title = book_title

    def get_author(self):
        return self.__author

    def set_author(self, author):
        self.__author = author

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_publication_date(self):
        return self.__publication_date

    def set_publication_date(self, publication_date):
        self.__publication_date = publication_date

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def get_dynamic_content(self):
        return self.__dynamic_content

    def set_dynamic_content(self, dynamic_content):
        self.__dynamic_content = dynamic_content
