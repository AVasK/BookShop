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
        self.env_exec_orders = []

        N_BOOKS = int(N_BOOKS)
        N_PUB = int(N_PUB)
        self.N_DAYS_STEP = int(N_DAYS_STEP)
        self.MAX_CUST_PER_DAY = int(MAX_CUST_PER_DAY)

        # Store:
        self.store = Store(usual_markup=usual_markup, novel_markup=new_markup, SHIPMENT_SIZE = int(PUB_SHIPMENT_SIZE))

        # Publishers:
        self.publishers = [PublisherGenerator.random() for _ in range(N_PUB-1)]
        #self.publishers.append( Publisher('NoStarchPress', WarehouseGenerator.random(6)) )

        # Store:
        self.store.pull_books(N_BOOKS)
        self.book_listing = self.store.books()

    def step(self):
        for _ in range(self.N_DAYS_STEP):
            self.simulate_day()
            ModelTime.time_step()
            self.store.check_orders()
            self.store.check_promises()

    def order_list(self):
        return self.store.get_orders()

    def promise_list(self):
        return self.store.get_promises()

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

        def exec_save_id(order):
            _id = order._id
            order.execute()
            return _id

        executed = [f"{id(o)}" for o in self.env_orders if o.ready()]
        for o in self.env_orders:
            if o.ready():
                o.execute()

        self.env_orders = [set_pending(o) for o in self.env_orders if not o.ready()]

        self.env_exec_orders = executed

        N_CUST = random.randint(1, self.MAX_CUST_PER_DAY) # N of customers per day
        for _ in range(N_CUST):
            self.simulate_customer()


def weighted_choice(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i

def book_weighting(books, importance_factor):
    importance = lambda book : [1, importance_factor][book.is_new()]
    return [importance(b) for b in books]

def choose_book(books, importance_factor = 10):
    book_weights = book_weighting(books, importance_factor)
    i = weighted_choice(book_weights)
    return books[i]
