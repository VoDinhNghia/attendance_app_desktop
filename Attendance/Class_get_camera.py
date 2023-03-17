import cv2
class get_Camera:
    @classmethod
    def getCam(cls, cam_str):
        if(cam_str.isnumeric and len(cam_str)==1):
            cap = cv2.VideoCapture(0)
        elif(len(cam_str)==0):
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(cam_str)
        return cap

    