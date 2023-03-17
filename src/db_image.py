from connect_db import ConnectDb
import os
from PIL import Image
import numpy as np 

class GetInfoImage:
    @classmethod
    def getImagesAndLabels(cls, path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
        faces = []
        idList = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg,'uint8')
            id = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            idList.append(id)
        return idList, faces
        
    @classmethod
    def getProfile(cls, id):
        connect, cursor = ConnectDb.connectMysql()
        query = 'select * from label_face where ID= %s'
        cursor.execute(query, str(id))
        connect.commit()
        results = cursor.fetchall() 
        profile = None
        for row in results:
            profile = row
        return profile

