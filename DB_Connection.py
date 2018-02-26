import sqlite3

class DB_Connection(object):

    connection = None

    def _open(self):
        self.connection = sqlite3.connect("kaffeeWaechter.db")

    def _close(self):
        self.connection.close()

    def executeQuery(self, query):
        self._open()
        cursor = self.connection.cursor()
        cursor.execute(query)
        resultTable = cursor.fetchall()
        self._close()

        return resultTable

    def executeNonQuery(self, query):
        self._open()
        cursor=self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        self._close()
