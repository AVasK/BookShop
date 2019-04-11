# BookStore class hierarchy:
import random
from modelTime import ModelTime
from order import Order
from publisher import Publisher
# from man import Man


class Warehouse:
    # class contains different books & stats
    THRESHOLD = 3 # N. of books when we ask publisher to send more.

    def __init__(self, books):

        books = list(books)
        self.count = {}
        self.rating = {}
        for book in books:
            self.rating[book] = 0
            if book in self.count.keys():
                self.count[book] += 1
            else:
                self.count[book] = 1

    def __str__(self):
        ans = ''
        for book in list(self.books()):
            lock = '\U0001f512' if not book.for_kids else ''
            ans += f"{str(book):10}{book.price:>5}$ <{self.count[book]:4}> {lock}\n"

        return ans

    def list_by_rating(self):
        books = list(self.rating.items())
        return sorted(books, key = lambda x : x[1], reverse = True)

    def books_by_genre(self, genre):
        books = list(self.books())
        return [b for b in books if b.genre == genre]

    def ratings_by_genre(self, genre):
        books = list(self.books())
        return (genre, [self.rating[b] for b in books if b.genre == genre])

    def __getitem__(self, idx):
        return tuple(self.books())[idx] # changed list -> tuple for immutability

    def books(self):
        return set(self.count.keys())

    def inc_rating(self, book):
        self.rating[book] += 1

    def add(self, book):
        if book in self.count.keys():
            self.count[book] += 1
        else:
            self.count[book] = 1

        return self

    def remove(self, book):
        if book in self.books() and self.count[book] > 0:
            self.inc_rating(book)
            self.count[book] -= 1
            return self.find(book = book)
        else:
            return None

    def list_books(self):
        return list(self.books())

    def list_new(self):
        return [book for book in self.books() if book.is_new()]

    def find(self, *, name = None, book = None):
        # Find by book's name
        if name is not None:
            for book in self.books():
                if book.name == name:
                    return book
            return None
        # or by book itself
        if book is not None:
            for _book in self.books():
                if book == _book:
                    return _book
            return None

    def in_stock(self, book):
        if self.count[book] > 0:
            return True
        else:
            return False

    def book_count(self, book):
        return self.count[book]

    def findall(self, name):
        return [book for book in self.books() if book.name == name]


class Book:
    DEFAULT_STORE = None
    # Contains the information you typically can extract from the book (including cover)
    def __init__(self, name, authors, publisher, year, genre, pages, price, for_kids = False, n_days_ago = 0, store=None):
        self.name = str(name)
        self.authors = tuple(authors)
        self.publisher = publisher
        self.year = int(year) # Redundant
        self.genre = genre
        self.pages = int(pages)
        self.price = price
        self.for_kids = bool(for_kids)
        self.time = ModelTime(ModelTime.y_to_d(self.year) + n_days_ago)


    @classmethod
    def reprice(cls, book, new_price):
        new_book = cls(book.name, book.authors, book.publisher, book.year, book.genre, book.pages, new_price, book.for_kids)
        new_book.time = book.time
        return new_book

    @classmethod
    def copy(cls, book):
        new_book = cls(book.name, book.authors, book.publisher, book.year, book.genre, book.pages, book.price, book.for_kids)
        new_book.time = book.time
        return new_book

    def book_to_POD(self):
        return [self.name, self.authors, self.price, self.publisher]

    def get_publisher(self):
        return self.publisher

    def get_price(self):
        return self.price

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return f"-> {self.name}{' <new> ' if self.is_new() else ''}\nАвторы: {', '.join(str(a) for a in self.authors)}\n"

    def is_new(self):
        return self.time.is_recent()

    def uptime(self):
        return self.time.time()

    # Requires Book.store attribute set in Environment
    def __repr__(self):
        return f"{' <new> ' if self.is_new() else ''}{self.name} | {', '.join(str(a) for a in self.authors)} | {self.price:,d}"

    def __hash__(self):
        return hash(self.name) ^ hash(self.year) ^ hash(self.authors) ^ hash(self.publisher)


class Store:
    AUTO_BUY = True

    def __init__(self, books = None, usual_markup = 0.15, novel_markup = 0.35, SHIPMENT_SIZE = 5):
        self.shelf = Warehouse(books) if books is not None else Warehouse([])
        self.orders = []
        self.promises = []
        self.usual_markup = usual_markup
        self.novel_markup = novel_markup
        self.SHIPMENT_SIZE = SHIPMENT_SIZE

    def pull_books(self, N_BOOKS = None):
        books = []
        if N_BOOKS is None:

            for p in Publisher.enlist():
                books += list(p.books)

            self.shelf = Warehouse(books * 5)
            return
        else:
            from itertools import chain
            all_books = list(chain.from_iterable([list(p.books) for p in Publisher.enlist()]))
            self.shelf = Warehouse([random.choice(all_books) for _ in range(N_BOOKS)])

    def get_real_price(self, book):
        book = self.shelf.find(book=book)
        if book is None:
            return 0
        price = book.get_price()
        markup = self.novel_markup if book.is_new() else self.usual_markup
        total = price + markup * price
        return int(total)

    def order(self, customer, orders : []):
        book_list = []

        for order in orders:
            # Author
            if hasattr(order, 'surname'):
                # searching most recent release among all publishers
                publishers = Publisher.enlist()  # all existing publishers
                most_recent = []
                for p in publishers:
                    books = p.booksByAuthor(order)
                    if books:
                        most_recent.append(books[0])
                # the most recent book:
                book = list(sorted(most_recent, key=lambda x: x.uptime()))[0]
                book = Book.reprice(book, self.get_real_price(book))
                book_list.append(book)
            else:
                # Book:
                book_list.append(Book.reprice(order, self.get_real_price(order)))

        order = Order(self, customer, book_list)

        # if the orders are processed simultaneously & automatically
        if self.AUTO_BUY:
            if not order:
                # order cannot be executed
                # and books need to be printed and delivered
                # self.orders is a queue for those orders.
                self.orders.append(order)
            else:
                # Buy it!
                # Order is executed
                order.execute()

        return order

    def add_order(self, order):
        self.orders.append(order)

    @staticmethod
    def promised_books(promises):
        books = []
        for promise in promises:
            books += promise.content()
        return books

    def check_promises(self):
        flag = False
        promise = self.promises[0] if self.promises else False
        while promise:
            flag = True
            p = promise.execute()
            for book in p:
                self.shelf.add(book)
            self.promises.pop(0)
            promise = self.promises[0] if self.promises else False

        return flag

    def check_orders(self):
        order = self.orders[0] if self.orders else False
        while order:
            order.execute()
            self.orders.pop(0)
            order = self.orders[0] if self.orders else False

    def buy(self, book):
        if self.shelf.remove(book):
            if self.shelf.book_count(book) <= self.shelf.THRESHOLD:
                # There aren't many books left
                # First, checking if we have ordered this book already:
                if book not in Store.promised_books(self.promises):
                    # need to ask publisher to print those books
                    pub = book.get_publisher()
                    self.promises.append(pub.print(book, qty = self.SHIPMENT_SIZE))
                    # Publisher will return a Promise() to deliver them in N days.

            return Book.copy(book) # Finally, a book is sold to the client.
        else:
            return None

    def books(self):
        return list(self.shelf.books())

    def get_orders(self):
        return list(self.orders)

    def get_promises(self):
        return list(self.promises)

    # Accessing Warehouse:
    def access_warehouse(self):
        return self.shelf


if __name__ == '__main__':
    # Consider this a unit-test)
    from dataGen import WarehouseGenerator, ManGenerator, BookGenerator, PublisherGenerator
    publisher1 = PublisherGenerator.random()
    publisher2 = Publisher('NoShitNoPress', WarehouseGenerator.random(4))
    store = Store()
    store.pull_books(10)

    bs = list(store.access_warehouse().books())
    books_chosen = [random.choice(bs) for _ in range(4)]
    store.orders.append(Order(store, ManGenerator.random(), books_chosen))
    store.check_orders()
