
from PyQt5.QtCore import pyqtSignal 
from PyQt5.QtWidgets import   QLabel , QPushButton ,  QHBoxLayout , QWidget ,  QVBoxLayout , QListView , QDialog , QDoubleSpinBox
from PyQt5.QtGui import QPixmap

class ArchiveWin(QWidget):

    switch_request = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.to_page1 = QPushButton("Go back to Home")
        self.to_page1.clicked.connect(self.to_back)
        self.main_layout.addWidget(self.to_page1)
        self.info_layout = QVBoxLayout()

        self.list_view = QListView()

        
        self.to_page1.setProperty("class","buttons")

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
        self.main_layout.addWidget(self.list_view)
        
        self.main_layout.addLayout(self.info_layout)


        self.initUI()

        
    def initUI(self):
        self.image_label = QLabel(self)
        pixmap = QPixmap("background2.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.lower()

        self.db_interactive_lay = QHBoxLayout()

        self.delete_from_db = QPushButton("🗑️")
        self.add_into_watched = QPushButton("Watched")
    
        self.db_interactive_lay.addWidget(self.delete_from_db)
        self.db_interactive_lay.addWidget(self.add_into_watched)

        self.delete_from_db.setProperty("class","buttons")
        self.add_into_watched.setProperty("class","buttons")
        
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





    def to_back(self):
        self.switch_request.emit()


    def resizeEvent(self, event):
        self.image_label.resize(self.size())


    
class RatingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rate this Series")  #rating dialog is opening a different window 
        layout = QVBoxLayout()                   

        self.label = QLabel("Select your score:")
        layout.addWidget(self.label)

        
        self.spin_box = QDoubleSpinBox()
        self.spin_box.setRange(0.0, 10.0)
        self.spin_box.setSingleStep(0.5)
        layout.addWidget(self.spin_box)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.accept) # self.accept is built-in method in QDialog its closes the window
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def get_value(self):
        return self.spin_box.value()