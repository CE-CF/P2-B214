import mysql.connector

#Function to insert string into middle of another string, used for checking file path
def insert_string_middle_video(str, word):
    return str[:31] + word + str[31:]

def insert_string_middle_snapshot(str, word):
    return str[:34] + word + str[34:]


#Insert new poi into table
def new(drone, latitude, longitude):
    try:
        connection = mysql.connector.connect(user='root', password='password', # Opretter forbindelse til MySQL databasen
                                            host='localhost',
                                            database='hive')
        
        cursor = connection.cursor()

        mySql_new_check_query = """SELECT video, COUNT(*) FROM hive.poi WHERE video = %s GROUP BY video"""

        converted_i = ''

        for i in range(6):
            converted_i = '{}'.format(i)
            video = (insert_string_middle_video('C:/Users/user/POI/Videos/Video_.mp4', converted_i),)
            cursor.execute(mySql_new_check_query, video)
            results = cursor.fetchall()
            row_count = cursor.rowcount
            print("number of affected rows: {}".format(row_count))
            if row_count == 0: break
        
        video = insert_string_middle_video('C:/Users/user/POI/Videos/Video_.mp4', converted_i)
        snapshot = insert_string_middle_snapshot('C:/Users/user/POI/Videos/Snapshot_.jpg', converted_i)
        
        print("%s does not exist"% video)
        
        mySql_new_query = """INSERT INTO hive.poi (drone, latitude, longitude, video, picture, spotted) 
                            VALUES (%s, %s, %s, %s, %s, CURRENT_TIME) """
        poi_data = (drone, latitude, longitude, video, snapshot)
        cursor.execute(mySql_new_query, poi_data)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to insert new POI to table: {}".format(error))
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")