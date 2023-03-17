class Accuracy:
    @classmethod
    def acc(cls, a, b):
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