from connect_db import ConnectDb
import os
from PIL import Image
import numpy as np 

class get_DB_image:
    @classmethod
    def getImagesAndLabels(cls, path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        faces=[]
        IDs=[]
        for imagePath in imagePaths:
            faceImg=Image.open(imagePath).convert('L')
            faceNp=np.array(faceImg,'uint8')
            ID=int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
        return IDs, faces
        
    @classmethod
    def getProfile(cls, id):
        conn, cur = ConnectDb.connectMysql()
        cmd="SELECT * FROM label_face WHERE ID= %s"
        cur.execute(cmd, str(id))
        conn.commit()
        cursor = cur.fetchall() 
        profile=None
        for row in cursor:
            profile=row
        return profile

