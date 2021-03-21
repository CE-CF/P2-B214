import mysql.connector
 
#Insert new drone into table
def insert(drone, state, latitude, longitude):
    try:
        connection = mysql.connector.connect(user='root', password='password', # Opretter forbindelse til MySQL databasen
                                            host='localhost',
                                            database='hive')
        
        cursor = connection.cursor()

        mySql_insert_query = """INSERT INTO drone (drone, state, latitude, longitude, time) 
                                VALUES (%s, %s, %s, %s, CURRENT_TIME) """

        drone_data = (drone, state, latitude, longitude)
        cursor.execute(mySql_insert_query, drone_data)
        connection.commit()
        print("Record inserted successfully into drone table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

#Update drone already in table
def update(drone, state, latitude, longitude):
    try:
        connection = mysql.connector.connect(user='root', password='password', # Opretter forbindelse til MySQL databasen
                                            host='localhost',
                                            database='hive')
        
        cursor = connection.cursor()

        mySql_update_query = """UPDATE hive.drone SET 
                                                    state = %s, 
                                                    latitude = %s, 
                                                    longitude = %s, 
                                                    time = CURRENT_TIME 
                                                    WHERE drone = %s """

        drone_data = (state, latitude, longitude, drone)
        cursor.execute(mySql_update_query, drone_data)
        connection.commit()
        print("Record successfully updated drone table")

    except mysql.connector.Error as error:
        print("Failed to update MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

#Delete specified drone from hive.drone
def delete(drone):
    try:
        connection = mysql.connector.connect(user='root', password='password', # Opretter forbindelse til MySQL databasen
                                            host='localhost',
                                            database='hive')
        
        cursor = connection.cursor()

        mySql_delete_query = """DELETE FROM hive.drone WHERE drone = %s"""
        
        drone_data = (drone,)
        cursor.execute(mySql_delete_query, drone_data)
        connection.commit()
        print("Record deleted successfully from drone table")

    except mysql.connector.Error as error:
        print("Failed to delete from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")