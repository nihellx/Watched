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

        
    def create_table(self): # image_url exist in table + imdb_rating. difference is between rating and imdb_rating is rating taking by user
        self.c.execute("""CREATE TABLE IF NOT EXISTS data(
                imdbID TEXT PRIMARY KEY, 
                title TEXT NOT NULL,
                type INT,
                rating REAL,
                year INT,
                episode TEXT,

                is_archived INTEGER DEFAULT 0
            )""") 
        self.conn.commit()

    def save_into_library(self, imdbID, title, rating,imdb_rating, genre,is_archived=0): #directly to library
            self.c.execute("SELECT * FROM data WHERE imdbID = ?", (imdbID,))
            
            self.c.execute("""
                INSERT INTO data (imdbID, title, rating, imdb_rating, type, is_archived)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(imdbID) DO UPDATE SET title = excluded.title, rating = excluded.rating,  type = excluded.type, is_archived = excluded.is_archived
                """,
             (imdbID, title, rating, imdb_rating, genre, is_archived))

            
            self.conn.commit()

    def searched_data_insert_data(self,imdbID,title,rating,year,genre,imdb_rating,image_url,is_archived=3): # for caching
        self.c.execute("SELECT * FROM data WHERE title = ? AND is_archived = ?",(title ,is_archived,))
        result = self.c.fetchone()
        if result is not None:   
            self.c.execute("SELECT * FROM data WHERE title = ? and is_archived = 3",(title,))
            return self.c.fetchall()
        
        self.c.execute("INSERT INTO data (imdbID,title,rating,year,genre,imdb_rating,image_url,is_archived) VALUES (? , ? , ? , ? , ? , ? , ? , ?)",
                       (imdbID,title,rating,year,genre,imdb_rating,image_url,is_archived,))
        self.conn.commit()


    def searched_data(self,title,is_archived=3):
        words = title.split()
        #split the words to add % beginning and end
        like_clauses = " AND ".join(["title LIKE ?" for _ in words])
        # creating for loop for like clauses cause we dont have info about how many words there is gonna be 
        query = f"SELECT * FROM data WHERE {like_clauses} AND is_archived = ?"
        # creating query and execute it at one
        params = [f"%{word}%" for word in words]
        # preparing parameters to execute it later on 
        params.append(is_archived)
        
        self.c.execute(query, tuple(params)) # turning it into tuple cause its expects as tuple 
        result = self.c.fetchone()
        if result is not None:
            self.c.execute(query, tuple(params))
            return self.c.fetchall()
        
        return result
    


    def save_into_mylist_from_arc(self, imdbID, title, rating,genre,episode=None,is_archived=1):
                
        
        imdbid = imdbID
        
        self.move_to_mylist(imdbid)
        
        
        self.conn.commit()

        self.refresh_data1.emit()

        self.c.execute("SELECT * FROM data WHERE imdbID = ?", (imdbID,))
                
        if self.c.fetchone() is None:
            self.c.execute("INSERT INTO data (imdbID, title,  rating ,genre, episode,is_archived) VALUES (?, ?, ?, ? , ?, ? )",
                            (imdbID, title, rating, genre,episode,is_archived))
            self.conn.commit()
        else:
            self.c.execute("UPDATE data SET rating = ? WHERE imdbID = ? ",(rating,imdbID,))
            self.conn.commit()

    def query(self):
        # self.c.execute("DELETE  FROM data ")
        # self.conn.commit()
        
        self.c.execute("SELECT * FROM data WHERE is_archived = 3")
        data = self.c.fetchall()
        return data



    def delete_from_library(self,imdbid,is_archived=3):
        if  imdbid is None:

            return

        self.query()
        #instead of deleting the data we are changing their places for better caching 
        self.c.execute("UPDATE data SET is_archived = ?   WHERE imdbID = ?",(is_archived,imdbid,))
        self.conn.commit()

            

        self.refresh_data.emit()
        self.refresh_data1.emit()

    def move_to_mylist(self,imdbid,is_archived=1):
        if  imdbid is None:
            return

        #instead of deleting the data we are changing their places for better caching 
        self.c.execute("UPDATE data SET is_archived = ? WHERE imdbID = ?",(is_archived,imdbid,))
        self.conn.commit()

            

        self.refresh_data.emit()
        self.refresh_data1.emit()



    def search_a_series(self,imdbID):
        self.c.execute("SELECT * FROM data WHERE imdbID = ?",(imdbID,))
        return self.c.fetchall()

    def list_of_series(self):
        self.c.execute("SELECT * FROM data WHERE is_archived = 0 ORDER BY rating DESC ")
        return self.c.fetchall()

    def list_of_mylist(self):
        self.c.execute("SELECT * FROM data WHERE is_archived = 1 ORDER BY rating DESC ")
        return self.c.fetchall()         