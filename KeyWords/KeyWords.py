import re
import math
import itertools

class Kword:
    def __init__(self, scriptFile, stopWordsFile):
        file = open(scriptFile,'r', encoding='utf8')
        self.text = file.read().lower()
        file.close()
        stopWordsFile = open(stopWordsFile, 'r', encoding='utf8')
        self.listToRemove = list()
        for word in stopWordsFile.readlines():
            self.listToRemove.append(word.replace("\n",""))
        stopWordsFile.close()
        self.punctuationList = [",", ".", ";", ":", "!", "?"]


    def removeUnsignificantWords(doc, wordsList):
        for word in wordsList:
            doc = doc.replace(word, "")
        return doc


    def addSpaceToPunctuation(self):
        for punctuation in self.punctuationList:
            self.text = self.text.replace(punctuation, " " + punctuation + " ")


    def textToBag(self):
        bag = list()
        for word in self.text.split():
            if word not in self.listToRemove:
                strippedWord = re.sub(r's\b', '', word)
                bag.append(strippedWord)
        return bag


    def bag1ToBag3(self,bag1):
        bag3 = list()
        for i in range(0,len(bag1)-3):
            bagItem = ""
            if bag1[i] not in self.punctuationList:
                bag3.append(bag1[i])
                bagItem = bag1[i]
                if bag1[i+1] not in self.punctuationList:
                    bagItem = bagItem + " " + bag1[i+1]
                    bag3.append(bagItem)
                    if bag1[i + 2] not in self.punctuationList:
                        bagItem = bagItem + " " + bag1[i + 2]
                        bag3.append(bagItem)
        return bag3


    def computeKeyWords(self, n):
        self.addSpaceToPunctuation()
        bag = self.textToBag()
        bag3 = self.bag1ToBag3(bag)
        freqDico = dict()
        for keyWord in bag3:
            if keyWord not in freqDico.keys():
                freqDico[keyWord] = 1
            else:
                freqDico[keyWord] += 1

        sortedwords = sorted(freqDico.items(), key=lambda x:x[1], reverse=True)
        return dict(itertools.islice(sortedwords, n))


class Comparer:
    def __init__(self,scriptFile,transcriptFiles, n):
        script = Kword(scriptFile, "stopWords.txt")
        self.scriptVector = script.computeKeyWords(n)
        self.transcriptVectors = dict()
        for transcriptFile in transcriptFiles:
            transcript = Kword(transcriptFile, "stopWords.txt")
            self.transcriptVectors[transcriptFile] = transcript.computeKeyWords(n)

        for transCript in transcriptFiles:
            print(self.compare(transCript))

    def compare(self, transcriptFile):
        space = self.buildSpace(transcriptFile)
        transcriptVector = self.transcriptVectors[transcriptFile]
        sum = 0
        for dimension in space:
            if (dimension in self.scriptVector.keys()) and (dimension in transcriptVector.keys()):
                sum += math.pow(self.scriptVector[dimension] - transcriptVector[dimension], 2)
            if (dimension in self.scriptVector.keys()) and not (dimension in transcriptVector.keys()):
                sum += math.pow(self.scriptVector[dimension], 2)
            if not (dimension in self.scriptVector.keys()) and (dimension in transcriptVector.keys()):
                sum += math.pow(transcriptVector[dimension], 2)
        return math.sqrt(sum)


    def buildSpace(self, transcriptFile):
        dimensions = list()
        for key in self.scriptVector.keys():
            dimensions.append(key)
        transcript = self.transcriptVectors[transcriptFile]
        for key in transcript:
            if key not in dimensions:
                dimensions.append(key)
        return dimensions

