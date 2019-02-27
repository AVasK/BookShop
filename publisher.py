from modelTime import ModelTime
import random

class Publisher:
    listing = []
    
    def __init__(self, name, books):
        self.name = str(name)
        self.books = set(books)
        self.__class__.listing.append(self)
        

    def __str__(self):
        books_str = '\n>'.join(str(b)+' ['+str(b.uptime())+']' for b in list(self.books))
        return f"{self.name}\n>{books_str}"
    
    def __repr__(self):
        return f"{self.name}"
    
    
    @classmethod
    def enlist(cls):
        return cls.listing
    
    
    def booksByAuthor(self, author):
        return list(sorted([book for book in self.books if author in book.authors], key=lambda x: x.uptime(), reverse = False))
    
    
    def print(self, book, qty):
        time = random.choice(list(range(1, 6)))
        return Promise([book] * qty, time)
        
        
class Promise:
    def __init__(self, books : [], time : int):
        self.books = list(books)
        self.timer = ModelTime.timer(time)
        
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
        
        
        
        