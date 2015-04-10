import nltk
import sklearn
import sys

class NLC:
    def __init__(self):
        self.separator = ","
    def load(self, filePath):
        f = open(filePath, "r")
        lines = f.readlines()
        data = []
        labels = []
        for line in lines:
            label = line.split(self.separator)[-1]
            data.append(line[:-(len(label)+1)])
            labels.append(label.replace("\n",""))
        self.data = data
        self.labels = labels
    def printDataset(self):
        print self.data,self.labels
    def setLanguage(self):
        self.language = "english"

nlc = NLC()
nlc.load(sys.argv[1])
nlc.printDataset()
