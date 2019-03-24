# A modelling environment for bookstore modelling.
from store import Book, Store
from dataGen import WarehouseGenerator, ManGenerator, BookGenerator, PublisherGenerator
from publisher import Publisher
from order import Order
from modelTime import ModelTime
import random

class Environment:
    
    def __init__(self, N_BOOKS, usual_markup, new_markup, N_PUB = 3, N_DAYS_STEP = 1):
        
        print('Env. Init.')
        
        N_BOOKS = int(N_BOOKS)
        N_PUB = int(N_PUB)
        self.N_DAYS_STEP = int(N_DAYS_STEP)
        
        # Store:
        self.store = Store(usual_markup=usual_markup, novel_markup=new_markup)
        
        # Books init with Store:
        Book.store = self.store
        
        # Publishers:
        self.publishers = [PublisherGenerator.random() for _ in range(N_PUB-1)]
        self.publishers.append( Publisher('NoStarchPress', WarehouseGenerator.random(6)) )
        
        # Store:
        self.store.pull_books(N_BOOKS)
        
        # ModelTime.timeStep(days = N_DAYS_STEP)
        
        print(Publisher.enlist())
        
        # o = store.order(ManGenerator.random(), [book, book, books[2]])
        self.book_listing = self.store.books()
        #books_chosen = [random.choice(bs) for _ in range(4)]
        #self.store.orders.append(Order(self.store, ManGenerator.random(), books_chosen))

        
    def step(self):
        ModelTime.timeStep(days = self.N_DAYS_STEP)
        self.store.check_orders()
        self.store.check_promises()
        
    def order_list(self):
        return self.store.getOrders()
    
    def promise_list(self):
        return self.store.getPromises()
    
    def get_books(self):
        return self.store.books()
    
    def simulate_customer(self):
        N = random.randint(1, 10) # Number of books the customer orders
        order = [random.choice(self.book_listing) for _ in range(N)]
        customer = ManGenerator.random()
        self.store.order(customer, order)
        
    def simulate_day(self):
        N_CUST = random.randint(1, 10) # N of customers
        for _ in range(N_CUST):
            self.simulate_customer()
        