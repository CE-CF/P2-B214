from .tableHandler import TableHandler
from .databaseHandler import DatabaseHandler

class Drone(TableHandler, DatabaseHandler):

    def __init__(self, DroneName, latitude, longitude):
        self.DroneName = DroneName
        self.latitude = latitude
        self.longitude = longitude
        super().__init__('drone')
    
    def insert(self):
        mySql_insert_query = super().insert_query(drone = self.DroneName, lat = self.latitude, long = self.longitude)
        drone_data = (self.DroneName,self.latitude,self.longitude)
        print(mySql_insert_query+"| inserted values are {}".format(drone_data))

    def update(self):
        mySql_update_query = super().update_query(drone = self.DroneName, latitude = self.latitude, longitude = self.longitude)
        print(mySql_update_query)
    
    def delete(self):
        mySql_delete_query = super().delete_query(drone = self.DroneName)
        print(mySql_delete_query)
    
