import mysql.connector

def fetchall(table):
    try:
            #Establish connection to datase through mysql.connector
            connection = mysql.connector.connect(user='root', password='password',
                                                host='localhost',
                                                database='hive')
            
            cursor = connection.cursor() 

            mySql_fetchall_query = """SELECT * FROM {}""".format(table)
            
            #Create tuple with values for the insert
            table = (table, )
            
            #Execute query with values inserted
            cursor.execute(mySql_fetchall_query)

            #Commit previously executed query
            num_columns = len(cursor.description)
            column_names = [i[0] for i in cursor.description]
            myTable = cursor.fetchall()
            
            dataDict = {}
            output = []
            counter = 0   
            for row in myTable:
                for x in range(len(column_names)):
                    if (x == 0):    
                        dataDict[column_names[x]] = row[x]
                        print(row[x])  
                        print("---------------------") 
                    else:
                        dataDict[column_names[x]] = row[x]
                        print(column_names[x],": ", row[x])
                output.append(dataDict.copy())
                print(output[counter])
                counter+=1 
                                         
                
    #Exception if there is a connection error, which diplays the error that occured
    except mysql.connector.Error as error:
        print("Failed to retreive info from MySQL table {}".format(error))

    #Finally statement that closes connection to the database after the query is either committed or an error occurs
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        
        return output 