import mysql.connector

#Function to insert string into middle of another string, used for checking file path
def insert_string_middle_video(str, word):
    return str[:26] + word + str[26:]


#Insert new poi into table
def stream(drone):
    try:
        connection = mysql.connector.connect(user='root', password='password', # Opretter forbindelse til MySQL databasen
                                            host='localhost',
                                            database='hive')
        
        cursor = connection.cursor()

        mySql_new_check_query = """SELECT video, COUNT(*) FROM hive.video WHERE video = %s GROUP BY video"""

        converted_i = ''

        for i in range(6):
            converted_i = '{}'.format(i)
            video = (insert_string_middle_video('C:/Users/user/Video/Video_.mp4', converted_i),)
            cursor.execute(mySql_new_check_query, video)
            results = cursor.fetchall()
            row_count = cursor.rowcount
            print("number of affected rows: {}".format(row_count))
            if row_count == 0: break
        
        video = insert_string_middle_video('C:/Users/user/Video/Video_.mp4', converted_i)
        
        print("%s does not exist"% video)
        
        mySql_new_query = """INSERT INTO hive.video (drone, video, received) 
                            VALUES (%s, %s, CURRENT_TIME) """
        video_data = (drone, video)
        cursor.execute(mySql_new_query, video_data)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to insert new video to table: {}".format(error))
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")