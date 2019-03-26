# A modelling environment for bookstore modelling.
from store import Book, Store
from dataGen import WarehouseGenerator, ManGenerator, BookGenerator, PublisherGenerator
from publisher import Publisher
from order import Order
from modelTime import ModelTime
import random

class Environment:
    
    def __init__(self, N_BOOKS, usual_markup, new_markup, N_PUB = 3, N_DAYS_STEP = 1, MAX_CUST_PER_DAY = 10, PUB_SHIPMENT_SIZE = 5):
        
        print('Env. Init.')
        
        self.env_orders = []
        
        N_BOOKS = int(N_BOOKS)
        N_PUB = int(N_PUB)
        self.N_DAYS_STEP = int(N_DAYS_STEP)
        self.MAX_CUST_PER_DAY = int(MAX_CUST_PER_DAY)
        
        # Store:
        self.store = Store(usual_markup=usual_markup, novel_markup=new_markup, SHIPMENT_SIZE = int(PUB_SHIPMENT_SIZE))
        
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
        for _ in range(self.N_DAYS_STEP):
            self.simulate_day()
            ModelTime.timeStep()
            self.store.check_orders()
            self.store.check_promises()
        
        
    def order_list(self):
        return self.store.getOrders()
    
    def promise_list(self):
        return self.store.getPromises()
    
    def get_books(self):
        return self.store.books()
    
    def simulate_customer(self):
        N = random.randint(1, 4) # Number of books the customer orders
        customer = ManGenerator.random()
        order = Order(self.store, customer, [choose_book(self.book_listing) for _ in range(N)])
        #self.store.add_order(self.store, customer, order)
        self.env_orders.append(order)
        
    def simulate_day(self):
        
        # all the orders that are ready should be executed
        def set_pending(order):
            order.status = 'pending'
            return order
        
        [o.execute() for o in self.env_orders if o.ready()]
        self.env_orders = [set_pending(o) for o in self.env_orders if not o.ready()] 
        
        N_CUST = random.randint(1, self.MAX_CUST_PER_DAY) # N of customers per day
        for _ in range(N_CUST):
            self.simulate_customer()
            

def choose_book(books, k = 1):
    books_w_new = books + [b for b in books if b.is_new()] * k
    return random.choice(books_w_new)
        