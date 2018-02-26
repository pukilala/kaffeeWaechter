import mysql.connector
from mysql.connector import errorcode

class DB_Connection(object):

    __host = None
    __user = None
    __password = None
    __database = None

    __session = None
    __connection = None

    def __init__(self, host='localhost', user='kaffee', password='trinker', database='kaffeeWaechter'):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    def _open(self):
        try:
            cnx = mysql.connector.connect(host=self.__host,
                                            user=self.__user,
                                            password = self.__password,
                                            database = self.__database)
            self.__connection = cnx
            self.__session = cnx.cursor(buffered=True)


        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Password falsch')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Dataenbank exitiert nicht')
            else:
                print('error')

    def _close(self):
        self.__session.close()
        self.__connection.close()

    def executeQuery(self, query):
        self._open()
        self.__session.execute(query)
        resultTable = self.__session.fetchall()
        self._close()

        return resultTable

    def executeNonQuery(self, query):
        self._open()
        self.__session.execute(query)
        self.__connection.commit()
        self._close()
