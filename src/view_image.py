from cv2 import*
import cv2
import os

class Xem_Image:
    def __init__(self, path, Id):
        self.path = path
        self.Id = Id

    def Xem(self):
        imagePaths=[os.path.join(self.path,f) for f in os.listdir(self.path)] 
        for imagePath in imagePaths:
            ID_xem_anh=int(os.path.split(imagePath)[-1].split('.')[1])
            if(ID_xem_anh == self.Id):
                img_xem_anh = cv2.imread(imagePath)
                cv2.imshow("Xem anh",img_xem_anh)
