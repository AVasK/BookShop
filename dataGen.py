from abc import ABC, abstractmethod
import random
from store import Book, Warehouse
from publisher import Publisher
import modelTime
import man


class DataGenerator:
    # abstract data generator class
    # @abstractmethod
    def __init__(self):
        # should generate needed entity
        pass
    

class ManGenerator(DataGenerator):

    @classmethod
    def random(cls, genName = False):
        name = cls.pick_name() if genName else None
        surname = cls.pick_surname()
        contact = cls.pick_contact()
        return man.Man(name=name, surname=surname, contact=contact)

    @staticmethod
    def pick_surname():
        surnames = ['0xDEADBEEF', 'Набоков', 'Горький', 'Толстой', 'Sur_101', 'Sur_102']
        return random.choice(surnames)

    @staticmethod
    def pick_name():
        names = ['I.', 'A.', 'V.', 'S.', 'O.']
        return random.choice(names)
    
    @staticmethod
    def pick_contact():
        
        import string  # imported on-demand
        
        def gen_phone():
            prefix_len = 2
            number_len = 7
            return '+79' + ''.join(str(random.randint(1, 9)) for _ in range(prefix_len + number_len))
        
        def gen_email():
            options = string.ascii_lowercase + string.digits
            providers = ['mail.ru', 'gmail.com', 'inbox.com']
            length = list(range(4, 12))
            L = random.choice(length)
            addr = ''.join(random.choice(options) for _ in range(L)) + '@' + random.choice(providers)
                
            return addr
        
        type_of = random.choice(['email', 'phone'])
        if type_of == 'email':
            return gen_email()
        else:
            return gen_phone()


class BookGenerator(DataGenerator):

    @classmethod
    def random(cls, pub = None):
        genres = ['комедия', 'драма', 'научная фантастика', 'фентези', 'научная литература']
        if pub is None:
            pub = cls.pick_pub()
            
        args = {
                'name': cls.gen_name(),
                'authors': cls.pick_authors(),
                'publisher': pub,
                'year': random.randint(1700, modelTime.Year),
                'genre': random.choice(genres),
                'pages': random.randint(20, 5000),
                'price': random.randint(10, 1000),
                'for_kids': random.choice((True, False)),
                'n_days_ago': random.randint(0, 200),
               }

        return Book(**args)

    @staticmethod
    def gen_name():
        names = ['Мат.Анализ I', 'Мат.Анализ II', 'Мат.Анализ III', 'Физика: Оптика', 'Электрод', 'Сказки про Мат.Анализ', 'Выучить С++ за 21 день']
        
        return random.choice(names)
    
    @staticmethod
    def pick_authors():
        N = random.randint(1, 3)
        return [ManGenerator.random(genName = True) for _ in range(N)]

    @staticmethod
    def pick_pub():
        pub = random.choice(Publisher.enlist()) if Publisher.enlist() else Publisher('SomePub', [])
        return pub
    

class WarehouseGenerator(DataGenerator):
    @classmethod
    def random(cls, N_books, pub = None):
        books = [BookGenerator.random(pub) for _ in range(int((N_books * 3/4)))]
        
        books_with_duplicates = [random.choice(books) for _ in range(N_books)]
        return Warehouse(books_with_duplicates)


class PublisherGenerator(DataGenerator):
    @staticmethod
    def random(books=None, DEF_N=20, GENERATE=True):
        names = ['AstPress', 'NoShitPress', 'Factoid']
        
        p = Publisher(random.choice(names), [])
        
        if books is None:
            books = list(WarehouseGenerator.random(DEF_N, p)) if GENERATE else []
        
        else:
            for i in range(len(books)):
                books[i].publisher = p
            
        p.books = set(books)
        
        return p
