from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Color(QWidget):
    def __init__(self, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAutoFillBackground(True) # fill widget BG with window's color
        
        palette = self.palette() # default palette
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
        
        
class BookWidget(Color):
    def __init__(self, name, authors, price, pub, qty, *args, **kwargs):
        super().__init__('white', *args, **kwargs)
        
        page = QVBoxLayout()
        layout = QGridLayout()
        
        text = QLabel('Book Info:')
        page.addWidget(text)
        font = text.font()
        font.setPointSize(30)
        text.setFont(font)
        
        layout.addWidget(QLabel('Name'), 0, 0)
        layout.addWidget(QLabel(name), 0, 1)
        
        layout.addWidget(QLabel('Author(s)'), 1, 0)
        row_n = 1
        for i, auth in enumerate(authors):
            layout.addWidget(QLabel(str(auth)), row_n + i, 1)
            
        row_n = row_n + i
        del(i)
        
        layout.addWidget(QLabel('Publisher'), row_n + 1, 0)
        layout.addWidget(QLabel(str(pub)), row_n + 1, 1)
        
        layout.addWidget(QLabel('Quantity'), row_n + 2, 0)
        layout.addWidget(QLabel(str(qty)), row_n + 2, 1)
        
        layout.addWidget(QLabel('Price'), row_n + 3, 0)
        layout.addWidget(QLabel(str(price)), row_n + 3, 1)
        
        page.addLayout(layout)
        self.setLayout(page)
        
        
class StatsTab(Color):
    def __init__(self, by_rating, ratings_by_genre , *args, **kwargs):
        super().__init__('white', *args, **kwargs)
        
        layout = QHBoxLayout()
        
        top = QListWidget()
        rate = [f"{b}\nRATING: {r}" for b, r in by_rating]
        top.addItems(rate)
        
        by_genre_stats = QListWidget()
        genre_wise_stats = [f"{g} : {r}" for g, r in ratings_by_genre]
        by_genre_stats.addItems(genre_wise_stats)
        
        layout.addWidget(top)
        layout.addWidget(by_genre_stats)
        
        self.setLayout(layout)
        
        
class SettingsTab(Color):
    
    fields = ['N_DAYS_STEP_widget', 'N_BOOKS_widget', 'N_PUB_widget', 'usual_markup_widget', 'new_markup_widget']
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__('lightgray', *args, **kwargs)
        
        self.parent = parent
        
        self.layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        settings1 = QVBoxLayout()
        settings2 = QVBoxLayout()
    
        self.N_DAYS_STEP_widget = QLineEdit()
        s1 = QHBoxLayout()
        s1.addWidget(QLabel("Шаг (в днях):"))
        s1.addWidget(self.N_DAYS_STEP_widget)
    
        s2 = QHBoxLayout()
        s2.addWidget(QLabel("Кол-во книг в начале:"))
        self.N_BOOKS_widget = QLineEdit()
        s2.addWidget(self.N_BOOKS_widget)
    
        s3 = QHBoxLayout()
        s3.addWidget(QLabel("Кол-во издательств:"))
        self.N_PUB_widget = QLineEdit()
        s3.addWidget(self.N_PUB_widget)
    
        s4 = QHBoxLayout()
        s4.addWidget(QLabel("Обычная наценка:"))
        self.usual_markup_widget = QLineEdit()
        s4.addWidget(self.usual_markup_widget)
    
        s5 = QHBoxLayout()
        s5.addWidget(QLabel("Наценка на новые:"))
        self.new_markup_widget = QLineEdit()
        s5.addWidget(self.new_markup_widget)
    
        settings1.addLayout(s1)
        settings1.addLayout(s2)
        settings1.addLayout(s3)
    
        settings2.addLayout(s4)
        settings2.addLayout(s5)
        self.btn = QPushButton('Сохранить настройки')
        self.btn.clicked.connect(self.save_settings)
        settings2.addWidget(self.btn)
    
        hlayout.addLayout(settings1)
        hlayout.addLayout(settings2)
        
        # Error message
        self.err_msg = QLabel("Настойки моделирования:")
        font = self.err_msg.font()
        font.setPointSize(25)
        self.err_msg.setFont(font)
        self.err_msg.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.err_msg)
        
        self.layout.addLayout(hlayout)
        self.setLayout(self.layout)
        
    def save_settings(self):
        self.err_msg.setText("Настойки моделирования:")
        
        def fields_filled(self):
            return not any(getattr(self, field).text() == '' for field in self.fields)
        
        if fields_filled(self):
            for field in self.fields:
                self.parent.settings[str(field)[:-7]] = float(getattr(self, field).text())
            
            self.parent.setup_complete = True
            self.parent.stats = False
            self.parent.settings_set()
            self.err_msg.setText("ОК")
        else:
            self.err_msg.setText("Не все поля заполнены!")
            
        

class DefaultModellingTab(Color):
    def __init__(self, *args, **kwargs):
        super().__init__('white', *args, **kwargs)
        
        layout = QVBoxLayout()
        text1 = QLabel("Чтобы начать моделирование\nзадайте настройки.")
        font = text1.font()
        font.setPointSize(30)
        text1.setFont(font)
        text1.setAlignment(Qt.AlignCenter)
        layout.addWidget(text1)
        self.setLayout(layout)
        
class ModellingTab(Color):
    def __init__(self, parent, *args, **kwargs):
        super().__init__('white', *args, **kwargs)
        
        self.parent = parent
        
        page = QVBoxLayout()
        layout = QHBoxLayout()
        column1 = QVBoxLayout()
        column2 = QVBoxLayout()
        column3 = QVBoxLayout()
        
        # Column 1
        column1.addWidget(QLabel("Store"))
        self.books_list = QListWidget()
        self.books_list.addItems([])
        column1.addWidget(self.books_list)
        
        self.books_list.itemDoubleClicked.connect(self.book_info)
        
        # Column 2
        column2.addWidget(QLabel("Orders"))
        self.orders_list = QListWidget()
        self.orders_list.addItems(['A', 'C', 'D', 'C'])
        column2.addWidget(self.orders_list)
        
        # Column 3
        column3.addWidget(QLabel("Pub. orders"))
        self.pub_orders_list = QListWidget()
        self.pub_orders_list.addItems(['D', 'C', 'F', 'G', 'H'])
        column3.addWidget(self.pub_orders_list)
        
        layout.addLayout(column1) # col1
        layout.addLayout(column2) # col2
        layout.addLayout(column3) # col3
        
        page.addLayout(layout)
        
        step_button = QPushButton("Шаг")
        step_button.clicked.connect(parent.step_callback)
        
        stop_button = QPushButton("Стоп")
        stop_button.clicked.connect(parent.stop_callback)
        
        page.addWidget(step_button)
        page.addWidget(stop_button)
        self.setLayout(page)
        
    
    def book_info(self, obj):
        #print(self.books_list.item(n))
        print(obj.text())
        row = self.books_list.currentRow()
        book = self.parent.books[row]
        desc = book.book_to_POD()
        desc.append(book.qty())
        
        self.pop_up = BookWidget(*desc)
        self.pop_up.setGeometry(QRect(500, 500, 400, 200))
        self.pop_up.show()
        
    def update_books(self, books):
        self.books_list.clear()
        self.books_list.addItems(books)
        
    def update_orders(self, orders):
        self.orders_list.clear()
        self.orders_list.addItems(orders)
        
    def update_pub_orders(self, promises):
        self.pub_orders_list.clear()
        self.pub_orders_list.addItems(promises)
        
        
class newWindow(QMainWindow):
    
    def __init__(self, callback, step_callback, stop_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.books = []
        
        self.callback = callback
        self.step_callback = step_callback
        self.stop_callback = stop_callback
        
        self.setup_complete = False
        self.settings = {}
        self.stats = False
        
        self.setWindowTitle('Colours!')
        
        self.tabs = QTabWidget()
        #self.tabs.setDocumentMode(True)
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)
        
        #tabs.addTab(Widget, name)
        self.tabs.addTab(SettingsTab(self), 'Параметры')
        self.modelling_tab = QStackedLayout()
        self.modelling_tab.addWidget(DefaultModellingTab())
        self.page_1 = ModellingTab(self)
        self.modelling_tab.addWidget(self.page_1)
        
        self.modelling_tab.setCurrentIndex(0)

        self.modelling_wget = QWidget()
        self.modelling_wget.setLayout(self.modelling_tab)
        
        self.tabs.addTab(self.modelling_wget, 'Моделирование')
        #self.tabs.addTab(OrderWidget(False, 'A', ['L.N.V',], 15, 3, 'Pub_unk'), 'Статистика')
        
        self.setCentralWidget(self.tabs)
        
        
    def settings_set(self):
        self.callback(**self.settings)
        self.step_callback()
        self.modelling_tab.setCurrentIndex(1)
        while self.tabs.count() >= 3:
            self.tabs.removeTab(2)
        self.tabs.setCurrentIndex(1)
        
    
    def update_books(self, books):
        self.books = books
        books = [str(b) for b in books]
        self.page_1.update_books(books)
        
    def update_promises(self, promises):
        self.page_1.update_pub_orders(promises)
    
    def update_orders(self, orders):
        self.page_1.update_orders(orders)
        
    def show_stats(self, rating, genre_rating):
        self.stats = True
        # optional
        while self.tabs.count() >= 3:
            self.tabs.removeTab(2)
        self.tabs.addTab(StatsTab(rating, genre_rating), 'Статистика')
        self.tabs.setCurrentIndex(2)
        
        

"""
app = QApplication([])

new_window = newWindow(print)
new_window.show()

app.exec_() # the event loop started.
"""

        
        