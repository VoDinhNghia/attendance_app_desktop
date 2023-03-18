from cv2 import*
import cv2
import os

class ViewImage:
    def __init__(self, path, id):
        self.path = path
        self.id = id

    def view(self):
        imagePaths = [os.path.join(self.path, f) for f in os.listdir(self.path)] 
        for imagePath in imagePaths:
            idImage = int(os.path.split(imagePath)[-1].split('.')[1])
            if(idImage == self.id):
                showImage = cv2.imread(imagePath)
                cv2.imshow('View image', showImage)
