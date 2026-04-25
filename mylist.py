
from PyQt5.QtCore import pyqtSignal , QObject
from PyQt5.QtWidgets import   QLabel , QPushButton ,  QHBoxLayout , QWidget ,  QVBoxLayout , QListView , QDialog , QDoubleSpinBox
from PyQt5.QtGui import QPixmap



class MyList(QWidget):

    switch_request = pyqtSignal()

    def __init__(self):
        super().__init__()


        self.main_layout = QVBoxLayout(self)
        self.to_main_page = QPushButton("Go back to Home")
        self.to_main_page.clicked.connect(self.to_back)
        self.main_layout.addWidget(self.to_main_page)
        self.info_layout = QVBoxLayout()

        self.list_view = QListView()

        self.main_layout.addWidget(self.list_view)
        
        self.main_layout.addLayout(self.info_layout)

        
        self.list_view.setStyleSheet("""
        QListView {
        background-color: #4256d4;  
        border: 2px solid #3d3d3d;   
        border-radius: 10px;         
        color: black;                
        padding: 5px; 
        font-size: 25px;              
        }
        """)          
        self.db_interactive_lay = QHBoxLayout()

        self.delete_from_db = QPushButton("🗑️")
        
    
        self.db_interactive_lay.addWidget(self.delete_from_db)
       

        self.delete_from_db.setProperty("class","buttons")
        
        
        self.main_layout.addLayout(self.db_interactive_lay)

        


        self.setStyleSheet('''
            QPushButton[class="buttons"] {
                font-size: 20px;                         
                padding: 10px;      
                background: #545fa8;
                color: solid black;
                border-radius:10px ;

                min-width : 80px;
                min-height: 60px;                                                         
            }
            QPushButton[class="buttons"]:hover {
                background: #6074f0;
            
            }
            QPushButton[class="buttons"]:pressed {
                background: #8692db;

            }    
        ''')
        self.initUI()

    def initUI(self):
        self.image_label = QLabel(self)
        pixmap = QPixmap("background2.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.lower()

        self.to_main_page.setProperty("class","buttons")

        self.setStyleSheet('''
            QPushButton[class="buttons"] {
                font-size: 20px;                         
                padding: 10px;      
                background: #545fa8;
                color: solid black;
                border-radius:10px ;

                min-width : 80px;
                min-height: 60px;                                                         
            }
            QPushButton[class="buttons"]:hover {
                background: #6074f0;
            
            }
            QPushButton[class="buttons"]:pressed {
                background: #8692db;

            }    
        ''')

    def to_back(self):
        self.switch_request.emit()

    def resizeEvent(self, event):
        self.image_label.resize(self.size())