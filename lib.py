import nltk
import sklearn.svm
import sys
from nltk.corpus import wordnet as wn

class Dataset:
    def __init__(self):
        self.separator = ","
        self.vectorData = []
        self.data = []
        self.labels = []
        self.wordDic = {}
    def loadTrain(self, filePath):
        f = open(filePath, "r")
        lines = f.readlines()
        for line in lines:
            label = line.split(self.separator)[-1]
            self.data.append(line[:-(len(label)+1)])
            self.labels.append(label.replace("\n",""))
    def loadTest(self, filePath):
        f = open(filePath, "r")
        lines = f.readlines()
        for line in lines:
            self.data.append(line.replace("\n",""))
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
    def vectorize(self, wordDic = None):
        if not wordDic:
            featureIndex = 0
            for sentence in self.data:
                for word in sentence:
                    if word not in self.wordDic:
                        self.wordDic[word] = featureIndex
                        featureIndex += 1
            wordDic = self.wordDic
        n = len(wordDic)
        for sentence in self.data:
            vec = [0]*n
            for word in sentence:
                if word in wordDic: vec[wordDic[word]] += 1
            self.vectorData.append(vec)

class Classifier:
    def __init__(self):
        self.clf = None
    def buildSVM(self, dataset, kernel = 'linear', c):
        if kernel == 'linear':
            self.clf = sklearn.svm.LinearSVC(C=c)
        else:
            self.clf = sklearn.svm.SVC(kernel = kernel,C=c)
        self.clf.fit(dataset.vectorData,dataset.labels)
    def predict(self, testset):
        print self.clf.predict(testset.vectorData)
    def test(self, testset, testlabels):
        preds = self.clf.predict(testset.vectorData)
        correct = sum(preds[i] == testlabels[i] for i in range(len(testlabels)))
        return float(correct)/len(testlabels)
    def mainWords(self, threshold):
        invVocab = {v: k for k, v in self.wordDic.items()}
        for i in range(len(self.clf.coef_[0])):
            c = self.clf.coef_[0][i]
            if abs(c) > threshold:
                print invVocab[i], c
        
    

ds = Dataset()
ds.setLanguage('english')
ds.loadTrain(sys.argv[1])
ds.tokenize()
ds.expandSynonyms()
ds.lowercase()
ds.stem()
ds.vectorize()

ts = Dataset()
ts.setLanguage('english')
ts.loadTest(sys.argv[2])
ts.tokenize()
ts.expandSynonyms()
ts.lowercase()
ts.stem()
ts.vectorize(ds.wordDic)

clf = Classifier()
clf.buildSVM(ds)
clf.predict(ts)
