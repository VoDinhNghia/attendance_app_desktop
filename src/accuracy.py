class Accuracy:
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