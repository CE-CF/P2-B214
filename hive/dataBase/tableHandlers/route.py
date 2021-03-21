from .tableHandler import TableHandler
from .databaseHandler import DatabaseHandler

class Route(TableHandler, DatabaseHandler):

    def __init__(self, DroneName, *routeCor):
        self.DroneName = DroneName
        self.routeCor = routeCor
        super().__init__('route')
    
    def insert(self):
        query_routeCor = ', '.join(str(v) for v in self.routeCor)
        mySql_insert_query = super().insert_query(*self.routeCor, drone = self.DroneName)
        drone_data = (self.DroneName, query_routeCor)
        print(mySql_insert_query+"| inserted values are {}".format(drone_data))

