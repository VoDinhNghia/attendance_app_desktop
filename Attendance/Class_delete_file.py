import os

class Delete_file:
    """
    Class use to delete file in folder.\n
    Lớp dùng để xóa file trong thư mục.
    """
    def __init__(self, path, Id):
        self.path = path
        self.Id = Id

    def delete(self):
        """
        Delete file on folder has ID equal with paramater ID.\n
        Xóa file trong thư mục có ID trùng với ID truyền vào.
        """
        imagePaths=[os.path.join(self.path,f) for f in os.listdir(self.path)]
        for imagePath in imagePaths:
            ID=int(os.path.split(imagePath)[-1].split('.')[1])
            if(ID == int(self.Id)):
                if(os.path.isfile(imagePath)):
                    os.remove(imagePath)