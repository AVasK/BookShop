from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from gui import newWindow
from Environment import Environment

class App:

    def __init__(self):
        self.env = None

        self.app = QApplication([])

        self.window = newWindow(self.env_setup, self.step, self.stop)

        self.window.show()

        self.app.exec_()

    def env_setup(self, *args, **kwargs):
        self.env = Environment(*args, **kwargs)
        self.window.store = self.env.store

    def step(self):
        self.env.step()

        orders = [str(o) for o in reversed(self.env.env_orders)]
        exec_orders = [str(i) for i in reversed(self.env.env_exec_orders)]
        promises = [str(p) for p in self.env.promise_list()]

        books = self.env.get_books()
        qty = [self.env.store.shelf.book_count(b) for b in books]
        books_w_qty = list(zip(books, qty))

        self.window.update_books(books_w_qty)
        self.window.update_orders(orders)
        self.window.update_executed_orders(exec_orders)
        self.window.update_promises(promises)

    def stop(self):
        rating = self.env.store.shelf.list_by_rating()
        from dataGen import BookGenerator
        from statistics import n_sold_by_genre
        genrewiserating = n_sold_by_genre(self.env.store.shelf.ratings_by_genre(genre) for genre in BookGenerator.genres)
        self.window.show_stats(rating, genrewiserating)


app = App()
