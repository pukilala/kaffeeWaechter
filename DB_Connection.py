import sqlite3

class DB_Connection(object):

    connection = None


    def __init__(self):
        self.connection = sqlite3.connect("kaffeeWaechter.db")    


    def _open(self):
        self.connection = sqlite3.connect("kaffeeWaechter.db")

    def _close(self):
        self.connection.close()

    def executeQuery(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        resultTable = cursor.fetchall()


        return resultTable

    def executeNonQuery(self, query):
        cursor=self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
