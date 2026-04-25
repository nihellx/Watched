import requests
from PyQt5.QtCore import pyqtSignal , QObject , Qt
from PyQt5.QtWidgets import   QLabel , QPushButton ,  QHBoxLayout , QWidget ,  QVBoxLayout 
from PyQt5.QtGui import QPixmap





class WidgetLoader(QObject):


    finished_loading = pyqtSignal(bytes)

    fetch_signal = pyqtSignal(str)

    
    def __init__(self,):
        super().__init__()
        self.fetch_signal.connect(self.fetch_image)

    def fetch_image(self, url):
            try:
                if url and url != "N/A":
                    response = requests.get(url)
                    self.finished_loading.emit(response.content)
            except Exception as e:
                print(f"Error loading image: {e}")




class SecondWindow(QWidget):

    switch_request = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.to_page1 = QPushButton("Go back to Home")
        self.to_page1.clicked.connect(self.to_back)
        self.to_page1.setProperty("class","buttons")        
    
        self.main_layout.addWidget(self.to_page1)
        self.info_layout = QVBoxLayout()


        self.interaction_but_lay = QHBoxLayout()
        self.archive_but = QPushButton("Add to Watchlist")
        self.watched_but = QPushButton("Add into Watched")


        



        self.interaction_but_lay.addWidget(self.archive_but)
        self.interaction_but_lay.addWidget(self.watched_but)
        


        self.main_layout.addLayout(self.info_layout)
        self.main_layout.addLayout(self.interaction_but_lay)

        




        self.initUI()


    def initUI(self):
        self.image_label = QLabel(self)
        pixmap = QPixmap("background2.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.lower()
        self.image_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        



    def creating_serie_info(self,value):

        w = QWidget()
        self.lay = QVBoxLayout(w)
        
        pixmap = QPixmap()
        response = requests.get(value['Poster'])
        pixmap.loadFromData(response.content)

        title_label  = QLabel(value.get('Title','Unknown Title'))
        year_label = QLabel(value.get('Year','Unknown Year'))
        rating_label = QLabel(value.get('imdbRating','x'))
        genre_label = QLabel(value.get('Genre','x'))

        poster_label = QLabel()
        poster_label.setPixmap(pixmap)
        poster_label.setFixedSize(250, 400)
        poster_label.setScaledContents(True)

        self.info_layout.addWidget(poster_label)
        self.info_layout.addWidget(title_label)
        self.info_layout.addWidget(year_label)
        self.info_layout.addWidget(rating_label)
        self.info_layout.addWidget(genre_label)

        title_label.setProperty("class","infolabel")
        year_label.setProperty("class", "infolabel")
        rating_label.setProperty("class", "infolabel")
        genre_label.setProperty("class", "infolabel")
        

        self.archive_but.setStyleSheet("""
            QPushButton{
                font-size: 25px;                         
                padding: 15px;      
                background: #4256d4;
                color: solid black;
                border-radius:50px ;

                min-width : 150px;
                min-height: 60px;                                                         
            }
            QPushButton:hover{
                background: #6074f0;
            
            }
            QPushButton:pressed {
                background: #8692db;

            }                 
        """)

        self.watched_but.setStyleSheet("""
            QPushButton{
                font-size: 25px;                         
                padding: 15px;      
                background: #4256d4;
                color: solid black;
                border-radius:50px ;

                min-width : 150px;
                min-height: 60px;                                                         
            }
            QPushButton:hover{
                background: #6074f0;
            
            }
            QPushButton:pressed {
                background: #8692db;

            }                 
        """)
        self.to_page1.setStyleSheet('''
            QPushButton {
                font-size: 20px;                         
                padding: 10px;      
                background: #545fa8;
                color: solid black;
                border-radius:10px ;

                min-width : 80px;
                min-height: 60px;                                                         
            }
            QPushButton:hover {
                background: #6074f0;
            
            }
            QPushButton:pressed {
                background: #8692db;

            }    
        ''')

        self.setStyleSheet("""
            QLabel[class="infolabel"] {
                font-size: 25px;                         
                padding: 15px;      
                background: #4256d4;
                color: black;
            }
        """)

        #self.main_layout.addLayout(self.lay)
        
        return w

    def resizeEvent(self, event):
        self.image_label.resize(self.size())

    def to_back(self):
        self.clear_layout(self.info_layout)
        self.switch_request.emit()


    def clear_layout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                        

