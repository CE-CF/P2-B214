import mysql.connector

class DatabaseHandler:

    def __init__(self):
        self.connection = self.connecter()
        self.cursor = self.getCursor()

    def connector(self):
        connection = mysql.connector.connect(user='root', password='password', host='localhost', database='hive')
        return connection
    
    def getCursor(self):
        return self.connection.cursor()
    
    def commit(self, query, data=None):
        if data == None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query,data)
        self.connection.commit()
    
    def closeConnection(self):
        if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")