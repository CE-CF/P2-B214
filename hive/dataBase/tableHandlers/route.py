import mysql.connector

#Function to insert string into middle of another string, used for checking file path
def insert_string_lat(str, word):
    return str[:3] + word

def insert_string_long(str, word):
    return str[:4] + word


#Insert new poi into table
def new(drone, type, *coordinates):
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
                type_converter = 'waypoint'
            else:
                type_converter = 'boundary'

            ds_list= ('drone', 'type, ')
            ending = (', received',)
            query_cor = [None]*len(coordinates)
            counter = 1
            for i in range(len(coordinates)):
                
                converted_counter = '{}'.format(counter)
                converted_counter2 = '{}'.format(counter-1)
                if (i % 2) == 0:
                    #print("{0} is Even".format(counter))
                    query_cor[i] = insert_string_lat('lat', converted_counter)
                    counter += 1
                else:
                    #print("{0} is Odd".format(counter))
                    query_cor[i] = insert_string_long('long', converted_counter2)

            query_placeholders = ', '.join(['%s'] * (len(coordinates)+2))
            query_columns = ', '.join(ds_list)
            query_cor = ', '.join(query_cor)
            query_end = ', '.join(ending)

            mySql_insert_route_query = ''' INSERT INTO hive.route (%s%s%s) VALUES (%s, CURRENT_TIME) ''' %(query_columns, query_cor, query_end, query_placeholders)

            #print(mySql_insert_route_query)
            dronetype = (drone,type_converter)
            route_data = dronetype+coordinates
            #print("this is my route_data: %s"% list(route_data))
            cursor.execute(mySql_insert_route_query, route_data)
            connection.commit()


        
        except mysql.connector.Error as error:
            print("Failed to insert new route to table: {}".format(error))
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
    else:
        print("Type not recognized, has to be in [1,2]")