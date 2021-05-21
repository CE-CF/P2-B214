import mysql.connector

"""
Variables needed in insert:
DroneName   (name of drone)
state       (offline, online)
position    (latitude, longitude)
routeType   (waypoint, boundary)
route       (lattitude and longitude array for route)
"""

#class TableHandler(MySQLConnection.conncetor):
class TableHandler:

    def __init__(self, table):
        self.table = table
        self.connection = self.connector()
        self.cursor = self.getCursor()

    #Function to insert string into middle of another string, used for generating column check
    def insert_string_lat(self, str, word):
        return str[:3] + word

    def insert_string_long(self, str, word):
        return str[:4] + word
    
    #Function to insert string into middle of another string, used for checking file path
    def insert_string_middle_video(self, str, word):
        return str[:31] + word + str[31:]

    def insert_string_middle_snapshot(self, str, word):
        return str[:34] + word + str[34:]
    
    def insert_string_middle_video2(self, str, word):
        return str[:26] + word + str[26:]

    def insert_query(self, *route, **insert):
        """either a normal insert query or a route insert query"""
        ds_list= (', '.join(['{}'.format(k) for k, w in insert.items()]))
        ending = (', received',)
        
        counter = 1
        route_data = 0
        for x in route:
                    for y in x:
                        route_data += 1
        route_data *= 2
        query_cor = [None]*route_data

        for i in range(route_data):
            
            converted_counter = '{}'.format(counter)
            converted_counter2 = '{}'.format(counter-1)
            if (i % 2) == 0:
                query_cor[i] = self.insert_string_lat('lat', converted_counter)
                counter += 1
            else:
                query_cor[i] = self.insert_string_long('long', converted_counter2)

        query_placeholders = ', '.join(['%s'] * (route_data+len(insert)))
        query_columns = ds_list
        query_cor = ', '.join(query_cor)
        query_end = ', '.join(ending)
        if len(query_cor) == 0:
            mySql_insert_query = """INSERT INTO hive.%s (%s%s) VALUES (%s, CURRENT_TIME)""" %(self.table, query_columns, query_end, query_placeholders)
        else :
            mySql_insert_query = """INSERT INTO hive.%s (%s, %s%s) VALUES (%s, CURRENT_TIME)""" %(self.table, query_columns, query_cor, query_end, query_placeholders)
        
        return mySql_insert_query

    def check_query(self, video):
        """ Insert video path to check for """
        mySql_check_query = """SELECT video, COUNT(*) FROM hive.%s WHERE video = '%s' GROUP BY video""" %(self.table, video)
        return mySql_check_query
    
    def route_check_query(self, latitude):
        """ Route check query"""
        mySql_route_check_query = """ SELECT * 
                                            FROM information_schema.COLUMNS
                                            WHERE 
                                                TABLE_SCHEMA = 'hive' 
                                            AND TABLE_NAME = 'route' 
                                            AND COLUMN_NAME = '%s' """%(latitude)
        
        return mySql_route_check_query

    def route_noColumn(self):
        mySql_route_noColumn = """ALTER TABLE hive.route 
                ADD COLUMN lat1 DECIMAL(10,6) AFTER type, 
                ADD COLUMN long1 DECIMAL(10,6) AFTER lat1 """
        
        return mySql_route_noColumn
    
    def route_withColumns(self):
        mySql_route_withColumns = """ALTER TABLE hive.route 
                    ADD COLUMN lat%s DECIMAL(10,6) AFTER long%s, 
                    ADD COLUMN long%s DECIMAL(10,6) AFTER lat%s"""
        
        return mySql_route_withColumns

    def update_query(self, **insert):
        ds_list= (', '.join(['{} = {!r}'.format(k, w) for k, w in insert.items()]),)
        where_statement = ', '.join(['{} = {!r}'.format(k, w) for k, w in list(insert.items())[:1]])
        query_placeholders = ', '.join(['%s'] * (len(insert)))
        query_columns = ', '.join(ds_list)

        mySql_update_query = ''' UPDATE hive.%s SET %s, received = CURRENT_TIME WHERE %s ''' %(self.table, query_columns, where_statement)
        print(mySql_update_query)
        return mySql_update_query

    def delete_query(self, **insert):
        where_statement = ', '.join(['{} = {!r}'.format(k, w) for k, w in list(insert.items())[:1]])
        mySql_delete_query = ''' DELETE FROM hive.%s WHERE %s ''' %(self.table, where_statement)
        print(mySql_delete_query)
        return mySql_delete_query
    

    def connector(self):
        connection = mysql.connector.connect(user='root', password='password', host='localhost', database='hive')
        return connection
    
    def getCursor(self):
        return self.connection.cursor()
    
    def commit(self, query, data=None):
        if data == None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)
        self.connection.commit()
    
    def execute(self, query, data=None):
        if data == None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)

    def fetchRow(self):
        self.cursor.fetchall()
        output = self.cursor.rowcount
        
        return output

    def closeConnection(self):
        if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")


