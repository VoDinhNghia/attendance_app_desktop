import cv2
class Camera:
    @classmethod
    def get(cls, cameraOption):
        if(cameraOption.isnumeric and len(cameraOption) == 1):
            cap = cv2.VideoCapture(0)
        elif(len(cameraOption) == 0):
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(cameraOption)
        return cap

    