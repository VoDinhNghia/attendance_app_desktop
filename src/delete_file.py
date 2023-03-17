import os

class Delete_file:
    def __init__(self, path, Id):
        self.path = path
        self.Id = Id

    def delete(self):
        imagePaths=[os.path.join(self.path,f) for f in os.listdir(self.path)]
        for imagePath in imagePaths:
            ID=int(os.path.split(imagePath)[-1].split('.')[1])
            if(ID == int(self.Id)):
                if(os.path.isfile(imagePath)):
                    os.remove(imagePath)