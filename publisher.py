from modelTime import ModelTime
import random


class Publisher:
    listing = []
    
    def __init__(self, name, books):
        self.name = str(name)
        self.books = set(books)
        self.__class__.listing.append(self)

    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return f"{self.name}"

    @classmethod
    def enlist(cls):
        return cls.listing

    def booksByAuthor(self, author):
        return list(sorted([book for book in self.books if author in book.authors], key=lambda x: x.uptime(), reverse = False))

    @staticmethod
    def print(book, qty):
        time = random.choice(list(range(1, 6)))
        return Promise([book] * qty, time)
        
        
class Promise:
    def __init__(self, books : [], time : int):
        self.books = list(books)
        self.timer = ModelTime.timer(time)
        
    def __str__(self):
        return str(self.books[0].name) + ' | ' + str(self.books[0].authors) + ' | ' + str(len(self.books)) + '\n' + str(self.books[0].publisher)
        
    def ready(self):
        return self.timer()
    
    def __bool__(self):
        return self.ready()
    
    def content(self):
        return self.books
    
    def execute(self):
        if self.timer():
            return self.books
        return False
