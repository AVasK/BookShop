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
        print('Callback')
        self.env = Environment(*args, **kwargs)
        
        
    def step(self):
        self.env.step()
        #self.env.simulate_day()
        
        orders = [str(o) for o in reversed(self.env.env_orders)]#reversed(self.env.order_list())]
        promises = [str(p) for p in self.env.promise_list()]
        books = self.env.get_books()
        
        self.window.update_books(books)
        self.window.update_orders(orders)
        self.window.update_promises(promises)
        
        
        
            
    def stop(self):
        rating = self.env.store.shelf.list_by_rating()
        from dataGen import BookGenerator
        from statistics import n_sold_by_genre
        genrewiserating = n_sold_by_genre(self.env.store.shelf.ratings_by_genre(genre) for genre in BookGenerator.genres)
        self.window.show_stats(rating, genrewiserating)
        
        
app = App()