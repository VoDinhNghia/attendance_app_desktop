import os

class DeleteFile:
    def __init__(self, path, id):
        self.path = path
        self.id = id

    def delete(self):
        imagePaths = [os.path.join(self.path, f) for f in os.listdir(self.path)]
        for imagePath in imagePaths:
            userId = int(os.path.split(imagePath)[-1].split('.')[1])
            if(userId == int(self.id)):
                if(os.path.isfile(imagePath)):
                    os.remove(imagePath)