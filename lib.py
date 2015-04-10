import nltk
import sklearn
import sys
from nltk.corpus import wordnet as wn

class NLC:
    def __init__(self):
        self.separator = ","
        self.vectorData = []
        self.data = []
        self.labels = []
    def load(self, filePath):
        f = open(filePath, "r")
        lines = f.readlines()
        for line in lines:
            label = line.split(self.separator)[-1]
            self.data.append(line[:-(len(label)+1)])
            self.labels.append(label.replace("\n",""))
    def printDataset(self):
        print self.data,self.labels
        if self.vectorData: print self.vectorData
    def setLanguage(self, language):
        self.language = language
    def expandSynonyms(self):
        for i in range(len(self.data)):
            x = self.data[i]
            synonyms = []
            for word in x:
                synonyms += [l.name() for s in wn.synsets(word) for l in s.lemmas()]
            self.data[i] += synonyms
            self.data[i] = list(set(self.data[i]))
    def tokenize(self):
        for i in range(len(self.data)):
            self.data[i] = nltk.word_tokenize(self.data[i])
    def lowercase(self):
        for i in range(len(self.data)):
            self.data[i] = [w.lower() for w in self.data[i]]
    def stem(self):
        stemmer = nltk.stem.snowball.SnowballStemmer(self.language)
        for i in range(len(self.data)):
            self.data[i] = [stemmer.stem(w) for w in self.data[i]]
    def vectorize(self):
        featureIndex = 0
        wordDic = {}
        for sentence in self.data:
            for word in sentence:
                if word not in wordDic:
                    wordDic[word] = featureIndex
                    featureIndex += 1
        n = len(wordDic)
        for sentence in self.data:
            vec = [0]*n
            for word in sentence:
                vec[wordDic[word]] += 1
            self.vectorData.append(vec)
        

nlc = NLC()
nlc.setLanguage('english')
nlc.load(sys.argv[1])
nlc.tokenize()
nlc.expandSynonyms()
nlc.lowercase()
nlc.stem()
nlc.vectorize()
nlc.printDataset()





