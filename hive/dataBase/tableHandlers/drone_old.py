import mysql.connector
 
def insert(drone, state, latitude, longitude):
    ''' Insert drone into hive.drone table with values stated 
        
        Parameters
        ----------
            drone: str
                Name of the drone                       | 'dronename'
            state: str
                State of the drone                      | 'Offline' / 'Online'
            latitude: float
                The latitude coordinates of the drone   | 11.111111
            longitude float
                The longitude coordinates of the drone  | 11.111111
    '''

    try:
        #Establish connection to datase through mysql.connector
        connection = mysql.connector.connect(user='root', password='password',
                                            host='localhost',
                                            database='hive')
        
        cursor = connection.cursor() 

        mySql_insert_query = """INSERT INTO hive.drone (drone, state, latitude, longitude, time) 
                                VALUES (%s, %s, %s, %s, CURRENT_TIME) """
        
        #Create tuple with values for the insert
        drone_data = (drone, state, latitude, longitude)
        
        #Execute query with values inserted
        cursor.execute(mySql_insert_query, drone_data)

        #Commit previously executed query
        connection.commit()
        print("Record inserted successfully into drone table")

    #Exception if there is a connection error, which diplays the error that occured
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    #Finally statement that closes connection to the database after the query is either committed or an error occurs
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def update(drone, state, latitude, longitude):
    ''' Update row where drone = drone with the values stated 
        
        Parameters
        ----------
            drone: str
                Name of the drone                       | 'dronename'
            state: str
                State of the drone                      | 'Offline' / 'Online' 
            latitude: float
                The latitude coordinates of the drone   | 11.111111
            longitude float
                The longitude coordinates of the drone  | 11.111111
    '''

    try:
        #Establish connection to datase through mysql.connector
        connection = mysql.connector.connect(user='root', password='password',
                                            host='localhost',
                                            database='hive')
        
        cursor = connection.cursor()

        mySql_update_query = """UPDATE hive.drone SET 
                                                    state = %s, 
                                                    latitude = %s, 
                                                    longitude = %s, 
                                                    time = CURRENT_TIME 
                                                    WHERE drone = %s """

        #Create tuple with values for the update
        drone_data = (state, latitude, longitude, drone)

        #Execute query with updated values
        cursor.execute(mySql_update_query, drone_data)

        #Commit previously executed query
        connection.commit()
        print("Record successfully updated drone table")
    
    #Exception if there is a connection error, which diplays the error that occured
    except mysql.connector.Error as error:
        print("Failed to update MySQL table {}".format(error))

    #Finally statement that closes connection to the database after the query is either committed or an error occurs
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def delete(drone):
    ''' Delete row where drone = drone 
        
        Parameters
        ----------
            drone: str
                Name of the drone | 'dronename'
    '''
    try:
        connection = mysql.connector.connect(user='root', password='password', # Opretter forbindelse til MySQL databasen
                                            host='localhost',
                                            database='hive')
        
        cursor = connection.cursor()

        mySql_delete_query = """DELETE FROM hive.drone WHERE drone = %s"""
        
        #Create tuple with drone that needs to be deleted
        drone_data = (drone,)

        #Execute query to delete row
        cursor.execute(mySql_delete_query, drone_data)
        connection.commit()
        print("Record deleted successfully from drone table")

    #Exception if there is a connection error, which display the error that occured
    except mysql.connector.Error as error:
        print("Failed to delete from MySQL table {}".format(error))

    #Finally statement that closes connection to the database after the query is either committed or an error occurs
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")