class Order:
    def __init__(self, store, customer, books):
        self.customer = customer
        self.books = list(books) # shallow copy made
        self.store = store
        self.status = ''
        
        total = 0
        for book in books:
            total += store.get_real_price(book)
        
        self.total = total
        
        self.store.add_order(self)

    def __str__(self):
        books_list = '\n+ '.join(f"{str(b.name) + ' - ' + str(', '.join(str(a) for a in b.authors)):<50} @\
                     {b.real_price()} rub." for b in self.books)
        return f"Клиент:\n|\n+ {self.customer}\n@ {self.customer.contact}\n|\nЗаказ:\n|\n+ " + books_list + \
               f"\n|\n__________\n[{self.total:^8}]\n{self.status}"

    # True when an order can be completed - i.e. when all books are in stock.
    def __bool__(self):
        if all(self.store.access_warehouse().in_stock(b) for b in self.books):
            return True
        else:
            return False
        
    def ready(self):
        if all(self.store.access_warehouse().in_stock(b) for b in self.books):
            return True
        else:
            return False
        
    def execute(self):
        if bool(self):
            print('order is executed')
            return [self.store.buy(b) for b in self.books]
        else:
            return None
