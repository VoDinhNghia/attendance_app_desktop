import cv2
class get_Camera:
    """
    Class handing parameter string to get device camera or streamer or video file mp4.\n
    Lớp xử lý chuỗi truyền vào để lấy camera thiết bị hoặc luồng stream hay video.
    """
    @classmethod
    def getCam(cls, cam_str):
        """
        Function return camera to recognition.\n
        Hàm trả về camera cần lấy để nhận dạng.
        """
        if(cam_str.isnumeric and len(cam_str)==1):
            cap = cv2.VideoCapture(0)
        elif(len(cam_str)==0):
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(cam_str)
        return cap

    