from Class_conn_DB import connect_DB
import os
from PIL import Image, ImageTk
import numpy as np 

class get_DB_image:
    """
    Class get data face and ID to trainning and return profile when predict.
    Lớp lấy dữ liệu face and ID để train và trả về profile khi dự đoán.
    """
    @classmethod
    def getImagesAndLabels(cls, path):
        """
        Function get list face image and ID in folder.\n
        Hàm lấy danh sách image face và ID trong thư mục.
        """
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
        """
        Function return profile such as ID and Name equal with parameter ID (ID predict).\n
        Hàm trả về profile mã số và name khi ID trùng với ID truyền vào (ID predict).
        """
        conn, cur = connect_DB.con_mysql()
        cmd="SELECT * FROM labelface WHERE ID= %s"
        #error not reltime
        cur.execute(cmd, str(id))
        conn.commit()
        cursor = cur.fetchall() 
        profile=None
        for row in cursor:
            profile=row
        #conn.close()
        return profile

