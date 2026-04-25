import requests
from PyQt5.QtCore import QObject , QAbstractListModel , Qt




base_url =  "http://www.omdbapi.com/?apikey=3d1ff693"    
    

class APIdb(QObject):
    def __init__(self):
        self.base_url =  "http://www.omdbapi.com/?apikey=3d1ff693"    
        self.serie_data = None
        self.details = None



    def get_the_data(self,name,index):
        url = f"{base_url}&s={name}"
        response = requests.get(url)
        if response.status_code == 200:
            self.serie_data = response.json()
    
        else:
            print(f"not have a match{response}")
            
    def get_the_detail(self,name):
        url = f"{base_url}&t={name}"
        response = requests.get(url)
        if response.status_code == 200:
            self.details =  response.json()
        return self.details


     
      
class MovieModel(QAbstractListModel):
    def __init__(self, movies=None):
        super().__init__()
        self.movies = movies or []
    def data(self, index, role):
        if role == Qt.DisplayRole:  #what will appear on screen
            movie = self.movies[index.row()]
            
            return f"{movie[1]}  |   {movie[2]}     |  ⭐ {movie[3]}  "
        return None

    def rowCount(self, index):

        return len(self.movies)
    





