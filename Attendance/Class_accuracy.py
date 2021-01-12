class Accuracy:
    """
    Class test accuracy of predict function in opencv.\n
    Lớp kiểm tra độ chính xác của opencv với tập ảnh test.
    """
    @classmethod
    def acc(cls, a, b):
        """
        Parameter such as two array constain ID in test dataset and ID in predict.\n
        Tham số truyền vào là 2 array ID trong tập test và ID trong predict.
        """
        d = a == b
        print(d)
        de = []
        dem = 0
        for i in d:
            if i==True:
                de.append(i)
                dem = dem+1
        acc = round((dem/len(a))*100,2)
        print("Đếm số phần tử đúng: ", dem)
        print("Độ chính xác là: {} %".format(acc))
        return acc