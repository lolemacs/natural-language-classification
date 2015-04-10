import nltk
import sklearn
import sys
from nltk.corpus import wordnet as wn

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
    def expandSynonyms(self):
        for i in range(len(self.data)):
            x = self.data[i]
            synonyms = []
            for word in x:
                synonyms += [l.name() for s in wn.synsets(word) for l in s.lemmas()]
            self.data[i] += synonyms
    def tokenize(self):
        for i in range(len(self.data)):
            self.data[i] = nltk.word_tokenize(self.data[i])
        

nlc = NLC()
nlc.load(sys.argv[1])
nlc.printDataset()
nlc.tokenize()
nlc.expandSynonyms()
nlc.printDataset()
