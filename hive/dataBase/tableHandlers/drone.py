import mysql.connector
from .tableHandler import TableHandler

class Drone(TableHandler):

    def __init__(self, DroneName, status, latitude, longitude):
        self.DroneName = DroneName
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
        super().__init__('drone')
    
    def insert(self):
        try:
            super().connector()
            super().getCursor()
            mySql_insert_query = super().insert_query(drone = self.DroneName, state = self.status,  latitude = self.latitude, longitude = self.longitude)
            drone_data = (self.DroneName, self.status, self.latitude, self.longitude)
            super().commit(mySql_insert_query, drone_data)
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        finally:

            super().closeConnection()

    def update(self):
        try: 
            super().connector()
            super().getCursor()
            mySql_update_query = super().update_query(drone = self.DroneName, state = self.status, latitude = self.latitude, longitude = self.longitude)
            super().commit(mySql_update_query)
        except mysql.connector.Error as error:
            print("Failed to update MySQL table {}".format(error))
        finally:
            super().closeConnection()
    
    def delete(self):
        try: 
            super().connector()
            super().getCursor()
            mySql_delete_query = super().delete_query(drone = self.DroneName)
            super().commit(mySql_delete_query)
        except mysql.connector.Error as error:
            print("Failed to delete MySQL table {}".format(error))
        finally:
            super().closeConnection()
    
