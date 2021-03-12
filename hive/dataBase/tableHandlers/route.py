import mysql.connector

#Function to insert string into middle of another string, used for checking file path
def insert_string_lat(str, word):
    return str[:3] + word

def insert_string_long(str, word):
    return str[:4] + word


#Insert new poi into table
def route(drone, type, *coordinates):
    lat_list = coordinates[::2]
    long_list = coordinates[1::2]
    if type in [1,2]:
        try:
            connection = mysql.connector.connect(user='root', password='password', # Opretter forbindelse til MySQL databasen
                                                host='localhost',
                                                database='hive')
            
            cursor = connection.cursor()

            mySql_route_check_query = """ SELECT * 
                                            FROM information_schema.COLUMNS
                                            WHERE 
                                                TABLE_SCHEMA = 'hive' 
                                            AND TABLE_NAME = 'route' 
                                            AND COLUMN_NAME = %s """

            converted_i = ''
            exist = 0
            noexist = 0

            for i in range(len(lat_list)):
                converted_i = '{}'.format(i+1)
                longtitude = (insert_string_long('long', converted_i),)
                cursor.execute(mySql_route_check_query, longtitude)
                results = cursor.fetchall()
                row_count = cursor.rowcount
                #print("number of affected rows: {}".format(row_count))
                if row_count == 1:
                    exist += 1
                if row_count == 0:
                    noexist += 1

            
            longitude = insert_string_long('long', converted_i)
            latitude = insert_string_lat('lat', converted_i)
            
            print("%i columns do exist"% exist)
            print("%i columns do not exist"% noexist)
            
            if exist == 0:
                mySql_route_new_query = """ALTER TABLE hive.route 
                ADD COLUMN lat1 DECIMAL(10,6) AFTER type, 
                ADD COLUMN long1 DECIMAL(10,6) AFTER lat1 """
                cursor.execute(mySql_route_new_query)
                connection.commit()
                exist += 1
                noexist -= 1
            
            for i in range(noexist):
                newvalue = i+1+exist
                lastvalue = i+exist
                new_cor = (newvalue, lastvalue, newvalue, newvalue)
                mySql_route_new_query = """ALTER TABLE hive.route 
                ADD COLUMN lat%s DECIMAL(10,6) AFTER long%s, 
                ADD COLUMN long%s DECIMAL(10,6) AFTER lat%s"""
                cursor.execute(mySql_route_new_query, new_cor)
                connection.commit()
            
            if type == 1:
                mySql_route_insert_info_query = """INSERT INTO hive.route (drone, type, received) 
                            VALUES (%s, %s, CURRENT_TIME) """
                type_converter = 'waypoint'
                info = (drone, type_converter)
                cursor.execute(mySql_route_insert_info_query, info)
                connection.commit()
            else:
                mySql_route_insert_info_query = """INSERT INTO hive.route (drone, type, received) 
                            VALUES (%s, %s, CURRENT_TIME) """
                type_converter = 'boundary'
                info = (drone, type_converter)
                cursor.execute(mySql_route_insert_info_query, info)
                connection.commit()
            
            for i in range(len(lat_list)):
                column = i+1
                mySql_route_insert_cor_query = """INSERT INTO hive.route (lat%s, long%s) 
                            VALUES (%s, %s) """
                cor = (column, column, lat_list[i], long_list[i])
                cursor.execute(mySql_route_insert_cor_query, cor)
                connection.commit()
            
        except mysql.connector.Error as error:
            print("Failed to insert new route to table: {}".format(error))
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
    else:
        print("Type not recognized")