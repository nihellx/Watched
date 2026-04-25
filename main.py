import sys
from ui import MainWindow
from api import APIdb , MovieModel
from ui2 import SecondWindow
from mylist import MyList 
from sqlite import DATABASE
from archive import ArchiveWin , RatingDialog
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtCore import QTimer 


class MainWin(MainWindow):
    def __init__(self):
        super().__init__()

        self.api = APIdb()
        self.page2 = SecondWindow()
        self.ml = MyList()
        self.archive_win = ArchiveWin()
        self.db = DATABASE(self)

        
        self.page2.switch_request.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.archive_win.switch_request.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.ml.switch_request.connect(lambda: self.stacked_widget.setCurrentIndex(0))    
    
        self.db.refresh_data.connect(lambda: self.load_archive(self.db.list_of_series()))
        self.db.refresh_data1.connect(lambda:self.load_mylist(self.db.list_of_mylist()))

        
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.archive_win)
        self.stacked_widget.addWidget(self.ml)


        self.archive_win.list_view.clicked.connect(self.get_selection)
        self.ml.list_view.clicked.connect(self._get_selection)        

        
        self.search_button.clicked.connect(self._on_watched)
        self.archive_button.clicked.connect(self._on_archive)
        self.mylist_button.clicked.connect(self._on_mylist)

        
        self.page2.watched_but.clicked.connect(lambda : self._rating_log("rate"))
        self.page2.archive_but.clicked.connect(self._add_into_archive)
    
        self.archive_win.add_into_watched.clicked.connect(lambda : self._rating_log("move"))
        

        self.archive_win.delete_from_db.clicked.connect(lambda: self.db.delete_from_library(self.imdb_id))
        self.ml.delete_from_db.clicked.connect(lambda: self.db.delete_from_library(self.imdb_id1))

        self.imdb_id = None
        self.imdb_id1 = None


    def _on_mylist(self):
        self.stacked_widget.setCurrentIndex(3)
        data = self.db.list_of_mylist()
        self.load_mylist(data)

    def _on_archive(self):
        self.stacked_widget.setCurrentIndex(2)
        data = self.db.list_of_series()
        self.load_archive(data)
        

    def _rating_log(self,type=None):
        rd = RatingDialog()
        
        if rd.exec():
            self.score = rd.get_value() #  for user rating  after clicked add to w
        if type == "rate":
            self._add_into_mylist()
        elif type == "move":
            self.add_into_mylist()
            


    def _on_watched(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)   # 1 sec timer
        self.timer.setSingleShot(True) #oneshot

        self.creating_linedit("search")              
        self.searching_lab.textChanged.connect(self.start_timer)  #on text change creating timer
        self.timer.timeout.connect(self.search) #end of the timer connecting signal




    def search(self):
        text = self.searching_lab.text()
        if not text : return  

        self.clear_layout(self.scrollayout)


        self.api.get_the_data(text,0)
        
        self.scrollayout.addStretch() 
        

        if 'Search' in self.api.serie_data:
            limit = 10  # searching data limit
            search_limit = min(len(self.api.serie_data['Search']),limit)  
            
            for i in range(search_limit):
                movie_data = self.api.serie_data['Search'][i]
                movie_rate = self.api.get_the_detail(self.api.serie_data['Search'][i]['Title'])['imdbRating']
                

                new_widget = self.creating_widget(movie_data,movie_rate)
            
                
                self.scrollayout.addWidget(new_widget)  

                self.title_button.clicked.connect(lambda checked,x=i: self.on_checked(x))   # we need to create a func with lambda cause otherwise we need
                                                                                            # to create different func for every single + buttons 

        self.scrollayout.addStretch()

    
    
    def start_timer(self):
        self.timer.start()  # func for timer start5

    def serie_instances(self,matches):
        for instance in matches:
            self.hbox.addWidget()
    def clear_layout(self,layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                        
    def on_checked(self,x):
        self.info = self.api.get_the_detail(self.api.serie_data['Search'][x]['Title'])
        value = self.page2.creating_serie_info(self.info)
        self.page2.info_layout.addWidget(value) 
        self.stacked_widget.setCurrentIndex(1)
        


    def _add_into_archive(self): # from search
        self.db.save_into_library(self.info["imdbID"],self.info["Title"],self.info["imdbRating"],self.info["Genre"],None,0)
        # different indexs end of the line is make seperate data places for data enterces
    def _add_into_mylist(self): # from search
        self.db.save_into_mylist_from_arc(self.info["imdbID"],self.info["Title"],self.score,self.info["Genre"],None,1) # difference is in mylist u can rate by urslf 

    def get_selection(self,index):
        self.imdb_id = self.archive_model.movies[index.row()][0]
        
    def _get_selection(self,index):
        self.imdb_id1 = self.mylist_model.movies[index.row()][0]


    def add_into_mylist(self): # from archive
        info = self.db.search_a_series(self.imdb_id)
        self.db.save_into_mylist_from_arc(info[0][0],info[0][1],self.score,info[0][2])
        

        
    def load_mylist(self, data):
        self.mylist_model = MovieModel(data)
        self.ml.list_view.setModel(self.mylist_model)

    def load_archive(self, data):
        self.archive_model = MovieModel(data)
        self.archive_win.list_view.setModel(self.archive_model)

app = QApplication(sys.argv)



window = MainWin() 
window.show()
sys.exit(app.exec_())




