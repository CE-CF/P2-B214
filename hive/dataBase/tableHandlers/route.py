import mysql.connector
from .tableHandler import TableHandler

class Route(TableHandler):

    def __init__(self, DroneName, routeType, *routeCor):
        self.DroneName = str(DroneName)
        self.routeCor = routeCor
        self.routeType = routeType
        super().__init__('route')
    
    def insert(self):
        lat_list = self.routeCor[::2]
        long_list = self.routeCor[1::2]
        if self.routeType in [0,1]:
            try:
                super().connector()
                super().getCursor()
                route_points = 0

                for x in self.routeCor:                         # Check how many points that are in the route
                    for y in x:
                        route_points += 1
                exist = 0
                noexist = 0
                for i in range(route_points):    
                    converted_i = '{}'.format(i+1)
                    longitude = (super().insert_string_long('long', converted_i),)
                    print("hertil?")
                    print(super().route_check_query(longitude))
                    super().execute(super().route_check_query(longitude))
                    row_count = super().fetchRow()
                    if row_count == 1:
                        exist += 1
                        print(exist)
                    if row_count == 0:
                        noexist += 1
                
                longitude = super().insert_string_long('long', converted_i)
                latitude = super().insert_string_lat('lat', converted_i)

                if exist == 0:
                    super().commit(super().route_noColumn())
                    exist += 1
                    noexist -= 1
                
                for i in range(noexist):
                    newvalue = i+1+exist
                    lastvalue = i+exist
                    new_cor = (newvalue, lastvalue, newvalue, newvalue)
                    mySql_route_withColumns = super().route_withColumns()
                    super().commit(mySql_route_withColumns, new_cor)
                
                if self.routeType == 0:
                    type_converter = 'waypoint'
                else:
                    type_converter = 'boundary'

                mySql_insert_query = super().insert_query(*self.routeCor, drone = self.DroneName, type = self.routeType)    # Generate insert query
                drone_type = (self.DroneName, type_converter)   # Define the insert arguments of the drone and type
                route_data = drone_type                         # Create a route_data tuple
                
                for x in self.routeCor:
                    for y in x:
                        route_data += tuple(y)    
                        
                super().commit(mySql_insert_query, route_data)  # execute and commit insert query
                print("Succesfully committed: "+mySql_insert_query)
                print("with values: {}".format(route_data))
                
            #Exception if there is a connection error, which display the error that occured
            except mysql.connector.Error as error:
                print("Failed to insert new route to table: {}".format(error))
            
            #Finally statement that closes connection to the database after the query is either committed or an error occurs
            finally:
                super().closeConnection()
        else:
            print("Type not recognized, has to be in [0,1]")