import sqlite3
from PyQt5.QtCore import  pyqtSignal , QObject







class DATABASE(QObject):

    refresh_data = pyqtSignal()
    refresh_data1 = pyqtSignal()

    def __init__(self,main):
        super().__init__()
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.create_table()
        self.main_w = main

        
    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS data(
                imdbID TEXT PRIMARY KEY, 
                title TEXT NOT NULL,
                type INT,
                rating REAL,
                episode TEXT,
                is_archived INTEGER DEFAULT 0
            )""") 
        self.conn.commit()

    def save_into_library(self, imdbID, title, rating, type,episode=None,is_archived=0):
            self.c.execute("SELECT * FROM data WHERE imdbID = ?", (imdbID,))
            
            if self.c.fetchone() is None:
                self.c.execute("INSERT INTO data (imdbID, title, rating ,type, episode,is_archived) VALUES (?, ?, ?, ?, ? , ?)",
                            (imdbID, title, rating, type,episode,is_archived))
                self.conn.commit()


    def save_into_mylist_from_arc(self, imdbID, title, rating, type,episode=None,is_archived=1):
                
        
        imdbid = imdbID
        self.delete_from_library(imdbid)

        self.conn.commit()

        self.refresh_data1.emit()

        self.c.execute("SELECT * FROM data WHERE imdbID = ?", (imdbID,))
                
        if self.c.fetchone() is None:
            self.c.execute("INSERT INTO data (imdbID, title, rating ,type, episode,is_archived) VALUES (?, ?, ?, ?, ? , ?)",
                            (imdbID, title, rating, type,episode,is_archived))
            self.conn.commit()






    def delete_from_library(self,imdbid):
        if  imdbid is not None:
            imdbID = imdbid
        
            self.c.execute("DELETE FROM data WHERE imdbID = ?",(imdbID,))
            self.conn.commit()

            self.refresh_data.emit()
            self.refresh_data1.emit()
        else:
            return 

    def search_a_series(self,imdbID):
        self.c.execute("SELECT * FROM data WHERE imdbID = ?",(imdbID,))
        return self.c.fetchall()

    def list_of_series(self):
        self.c.execute("SELECT * FROM data WHERE is_archived = 0 ORDER BY rating DESC ")
        return self.c.fetchall()

    def list_of_mylist(self):
        self.c.execute("SELECT * FROM data WHERE is_archived = 1 ORDER BY rating DESC ")
        return self.c.fetchall()         