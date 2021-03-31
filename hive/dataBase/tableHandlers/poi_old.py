import mysql.connector

def insert_string_middle_video(str, word):
    '''Function to insert string into middle of another string, used for checking file path'''
    return str[:31] + word + str[31:]

def insert_string_middle_snapshot(str, word):
    '''Function to insert string into middle of another string, used for checking file path'''
    return str[:34] + word + str[34:]


#Insert new poi into table
def new(drone, latitude, longitude):
    ''' Insert poi into hive.poi table with values stated 
        
        Parameters
        ----------
            drone: str
                Name of the drone                       | 'dronename'
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

        #create query that checks how many rows have the name specified under the video column
        mySql_new_check_query = """SELECT video, COUNT(*) FROM hive.poi WHERE video = %s GROUP BY video"""

        converted_i = ''

        #Loop that checks how many video files that have been created and breaks when it encounters a spot open
        for i in range(100):
            converted_i = '{}'.format(i)
            video = (insert_string_middle_video('C:/Users/user/POI/Videos/Video_.mp4', converted_i),)
            cursor.execute(mySql_new_check_query, video)
            results = cursor.fetchall()
            row_count = cursor.rowcount
            print("number of affected rows: {}".format(row_count))
            if row_count == 0: break
        
        #Creates new filepaths for video and snapshot
        video = insert_string_middle_video('C:/Users/user/POI/Videos/Video_.mp4', converted_i)
        snapshot = insert_string_middle_snapshot('C:/Users/user/POI/Videos/Snapshot_.jpg', converted_i)
        
        print("%s does not exist"% video)
        

        mySql_new_query = """INSERT INTO hive.poi (drone, latitude, longitude, video, snapshot, received) 
                            VALUES (%s, %s, %s, %s, %s, CURRENT_TIME) """

        #Create tuple with values for the insert
        poi_data = (drone, latitude, longitude, video, snapshot)

        #Execute query with values inserted
        cursor.execute(mySql_new_query, poi_data)

        #Commit previously executed query
        connection.commit()

    #Exception if there is a connection error, which display the error that occured
    except mysql.connector.Error as error:
        print("Failed to insert new POI to table: {}".format(error))
    
    #Finally statement that closes connection to the database after the query is either committed or an error occurs
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")