import mysql.connector
from .tableHandler import TableHandler

class Poi(TableHandler):

    def __init__(self, DroneName, latitude, longitude):
        self.DroneName = DroneName
        self.latitude = latitude
        self.longitude = longitude
        super().__init__('poi')
    
    def insert(self):
        try:
            super().connector()
            super().getCursor()
            for i in range(100):
                converted_i = '{}'.format(i)
                videoTaken = super().insert_string_middle_video('C:/Users/user/POI/Videos/Video_.mp4', converted_i)
                mySql_check_query = super().check_query(videoTaken)
                super().execute(mySql_check_query)
                row_count = super().fetchRow()
                print("row number {0} have {1} matching names".format(converted_i, row_count))
                if row_count == 0: 
                    break
            
            videoTaken = super().insert_string_middle_video('C:/Users/user/POI/Videos/Video_.mp4', converted_i)
            snapshotTaken = super().insert_string_middle_snapshot('C:/Users/user/POI/Videos/Snapshot_.jpg', converted_i)

            mySql_insert_query = super().insert_query(drone = self.DroneName, latitude = self.latitude, longitude = self.longitude, video = videoTaken, snapshot = snapshotTaken)
            drone_data = (self.DroneName,self.latitude,self.longitude,videoTaken,snapshotTaken)
            print(mySql_insert_query)
            print(drone_data)

            super().commit(mySql_insert_query, drone_data)
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        finally:
            super().closeConnection()