import mysql.connector

#Function to insert string into middle of another string, used for checking file path
def insert_string_middle_video(str, word):
    '''Function to insert string into middle of another string, used for checking if video exists'''
    return str[:26] + word + str[26:]


#Insert new poi into table
def stream(drone):
    ''' Insert video file path into hive.video table
        
        Parameters
        ----------
            drone: str
                Name of the drone                       | 'dronename'
    '''
    try:
        #Establish connection to datase through mysql.connector
        connection = mysql.connector.connect(user='root', password='password', # Opretter forbindelse til MySQL databasen
                                            host='localhost',
                                            database='hive')
        
        cursor = connection.cursor()

        #Create a check query to see how many video's are in the table
        mySql_new_check_query = """SELECT video, COUNT(*) FROM hive.video WHERE video = %s GROUP BY video"""

        converted_i = ''

        #Check how many videos are in the table
        for i in range(6):
            converted_i = '{}'.format(i)
            video = (insert_string_middle_video('C:/Users/user/Video/Video_.mp4', converted_i),)
            cursor.execute(mySql_new_check_query, video)
            results = cursor.fetchall()
            row_count = cursor.rowcount
            print("number of affected rows: {}".format(row_count))
            if row_count == 0: break
        
        #Create string with a video name not already present in the table
        video = insert_string_middle_video('C:/Users/user/Video/Video_.mp4', converted_i)
        
        print("%s does not exist"% video)
        
        #Create insert query
        mySql_new_query = """INSERT INTO hive.video (drone, video, received) 
                            VALUES (%s, %s, CURRENT_TIME) """
        
        #Create tuples with values for the insert
        video_data = (drone, video)
        
        #Execute query with values inserted
        cursor.execute(mySql_new_query, video_data)
        
        #Commit previously executed query
        connection.commit()
    
    #Exception if there is a connection error, which display the error that occured
    except mysql.connector.Error as error:
        print("Failed to insert new video to table: {}".format(error))
    
    #Finally statement that closes connection to the database after the query is either committed or an error occurs
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")