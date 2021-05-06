from .tableHandler import TableHandler

class Video(TableHandler):

    def __init__(self, DroneName):
        self.DroneName = DroneName
        super().__init__('video')
    
    #Function to insert string into middle of another string, used for checking file path
    def insert_string_middle_video(str, word):
        return str[:31] + word + str[31:]

    def insert_string_middle_snapshot(str, word):
        return str[:34] + word + str[34:]

    def insert(self):
        #for i in range(100):
        #    converted_i = '{}'.format(i)
        #    videoTaken = (self.insert_string_middle_video('C:/Users/user/POI/Videos/Video_.mp4', converted_i),)
        #    mySql_check_query = super().check_query(video)
        #    print(mysql_check_query)
        
        #videoTaken = self.insert_string_middle_video('C:/Users/user/POI/Videos/Video_.mp4', converted_i)
        #snapshotTaken = self.insert_string_middle_snapshot('C:/Users/user/POI/Videos/Snapshot_.jpg', converted_i)
        videoTaken = 'C:/Users/user/Video/Video_1.mp4'

        mySql_insert_query = super().insert_query(drone = self.DroneName, video = videoTaken)
        drone_data = (self.DroneName,videoTaken)
        print(mySql_insert_query+"| inserted values are {}".format(drone_data))
