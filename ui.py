import requests
from PyQt5.QtWidgets import  QMainWindow , QLabel , QPushButton , QLineEdit , QHBoxLayout , QWidget , QScrollArea  , QVBoxLayout , QStackedWidget 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt , QThread
from ui2 import WidgetLoader




                             



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()      #creating stacked widget for change screens between profile ,search etc
        self.setCentralWidget(self.stacked_widget)
        
        self.main_page = QWidget()
        self.main_page_layout = QVBoxLayout(self.main_page)

        self.stacked_widget.addWidget(self.main_page)
      

        self.setWindowTitle("Watched")
        self.setFixedSize(1200,900)

        self.initUI()
    
        self.setup_worker()

    def initUI(self):
        self.image_label = QLabel(self.main_page)
        pixmap = QPixmap("background2.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.lower()
        self.stacked_widget.setCurrentIndex(1)
       
        
        



        top_bar_layout = QHBoxLayout()
    
      
    
        self.profile_button = QPushButton('Profile')
        self.search_button = QPushButton('Search',)
        self.mylist_button  = QPushButton('My List')             
        self.archive_button = QPushButton('Archive')



        top_bar_layout.addWidget(self.search_button,alignment=Qt.AlignTop)
        top_bar_layout.addWidget(self.mylist_button,alignment=Qt.AlignTop)
        top_bar_layout.addWidget(self.archive_button,alignment=Qt.AlignTop)
        top_bar_layout.addWidget(self.profile_button,alignment=Qt.AlignTop)   

        
        self.main_page_layout.addLayout(top_bar_layout)    


        

        self.scrollarea = QScrollArea()  # scrollarea is a widget but cannot put into layout directly but layout needs QWidget for that reason u we use setwidget 
        self.scrollwidget = QWidget()

        self.scrollwidget.setStyleSheet("background: transparent;")
       

        self.scrollarea.setFixedSize(850,670)
        self.scrollarea.setWidgetResizable(True) # its necessary cause scroll u cant scroll without it

        self.scrollayout = QVBoxLayout(self.scrollwidget)
        self.scrollarea.setWidget(self.scrollwidget)
        


        self.searching_lab = QLineEdit()
        searching_lay = QHBoxLayout()        
        self.searching_lab.setPlaceholderText("Enter ur Serie")
        self.searching_lab.setFixedSize(300,50)
        
        self.searching_lab.hide()
        
        searching_lay.addWidget(self.searching_lab,alignment=Qt.AlignTop)

        self.main_page_layout.addLayout(searching_lay)                                             
              
        
        self.main_page_layout.addWidget(self.scrollarea,alignment=Qt.AlignRight | Qt.AlignBottom)

        
     
        
        self.searching_lab.setStyleSheet("""
                QLineEdit   {
                    font-size: 15px;                     
                    background: #719ed1;
                    color: white;                     
                }
         """)

        

        self.scrollarea.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 120);
                border-radius: 5px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 180);
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """) 

      
        self.search_button.setStyleSheet("""
            QPushButton {
                font-size: 25px;                         
                padding: 15px;      
                background: #4256d4;
                color: solid black;
                border-radius:50px ;

                min-width : 150px;
                min-height: 60px;                                                         
            }
            QPushButton:hover {
                background: #6074f0;
            
            }
            QPushButton:pressed {
                background: #8692db;

            }                 
        """)
        self.profile_button.setStyleSheet("""
            QPushButton {
                font-size: 25px;                         
                padding: 15px;      
                background: #4256d4;
                color: solid black;
                border-radius:50px ;

                min-width : 150px;
                min-height: 60px;                                                         
            }
            QPushButton:hover {
                background: #6074f0;
            
            }
            QPushButton:pressed {
                background: #8692db;

            }                 
        """)
        self.mylist_button.setStyleSheet("""
            QPushButton {
                font-size: 25px;                         
                padding: 15px;      
                background: #4256d4;
                color: solid black;
                border-radius:50px ;

                min-width : 150px;
                min-height: 60px;                                                         
            }
            QPushButton:hover {
                background: #6074f0;
            
            }
            QPushButton:pressed {
                background: #8692db;

            }                 
        """)
        self.archive_button.setStyleSheet("""
            QPushButton {
                font-size: 25px;                         
                padding: 15px;      
                background: #4256d4;
                color: solid black;
                border-radius:50px ;

                min-width : 150px;
                min-height: 60px;                                                         
            }
            QPushButton:hover {
                background: #6074f0;
            
            }
            QPushButton:pressed {
                background: #8692db;

            }    
             
        """)
        
    def setup_worker(self):
        self.threadx = QThread()

        self.worker = WidgetLoader()

        self.worker.moveToThread(self.threadx)

        self.worker.finished_loading.connect(self.update_ui_with_image)

        self.threadx.start()

    def creating_widget(self,film_data,imdb_rate):
 
        
        container = QWidget()
        self.layout_wid = QHBoxLayout(container)

        self.title_button  = QPushButton(film_data.get('Title','Unknown Title'))
        year_label = QLabel(film_data.get('Year','Unknown Year'))
        if imdb_rate != "N/A":
            self.imdb_rate = QLabel(f"⭐ {imdb_rate}")
        else:
            self.imdb_rate = QLabel("-")
        
        image_data = film_data.get('Poster',None)
        
        if image_data:
            self.worker.fetch_signal.emit(image_data)



        
        self.layout_wid.addWidget(self.title_button)
        self.layout_wid.addWidget(year_label)
        self.layout_wid.addWidget(self.imdb_rate)
        

        container.setFixedHeight(80)
        container.setFixedWidth(800)


        year_label.setStyleSheet("""
            QLabel {
                font-size: 20px;                         
                padding: 10px;      
                background: #4256d4;
                color: solid black;
                border-radius:10px ;

                min-width : 80px;
                min-height: 60px;                                                         
            }
        """)
        self.imdb_rate.setStyleSheet("""
            QLabel {
                font-size: 20px;                         
                padding: 10px;      
                background: #b39227;
                color: solid black;
                border-radius:10px ;

                min-width : 80px;
                min-height: 60px;                                                         
            }
        """)

        self.title_button.setStyleSheet('''
            QPushButton {
                font-size: 20px;                         
                padding: 10px;      
                background: #4256d4;
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

        

        return container

    def creating_linedit(self,type):
        if type == "search":
            self.searching_lab.show()
            self.searching_lab.raise_()           


    def resizeEvent(self, event):
        self.image_label.resize(self.size())
        super().resizeEvent(event)

    

    def update_ui_with_image(self,image_data):
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setFixedSize(80, 80)
        image_label.setScaledContents(True)
   
        self.layout_wid.addWidget(image_label)