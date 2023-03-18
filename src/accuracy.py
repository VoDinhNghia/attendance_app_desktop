from tkinter import messagebox
import cv2
from cv2 import *
import numpy as np
from db_image import GetInfoImage

class Accuracy:
    def __init__(self, recognizer):
        self.recognizer = recognizer

    def show(self):
        pathFolderImageTest = 'image_test'
        idLists, faceLists = GetInfoImage.getImagesAndLabels(pathFolderImageTest) 
        resultPredict = []
        for img in faceLists:
            gray = cv2.fastNlMeansDenoising(img, None, 4, 5, 11)
            predict, conf = self.recognizer.predict(gray)
            resultPredict.append(predict)
        resultCalculate = self.calculate(np.array(idLists), np.array(resultPredict))
        messagebox.showinfo('message','Accuracy of 100 image test is: '+str(resultCalculate) + '%')

    @classmethod
    def calculate(cls, idListTest, idListPredict):
        isListCheck = idListTest == idListPredict
        numberCorrect = 0
        for i in isListCheck:
            if i == True:
                numberCorrect = numberCorrect + 1
        accuracy = round((numberCorrect / len(idListTest)) * 100, 2)
        print("correct element is: ", numberCorrect)
        print("accuracy is: {} %".format(accuracy))
        return accuracy