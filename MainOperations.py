import docx
import glob2
import math
import os

NbPositive = 0
NbNegative = 0

Path = os.getcwd() + r"\DataSet"
acceptableChars = ["a","b","c","d","e","f","g","h","i","î","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
                   "é", "è","ê", "à","â", "û", "ô", "'","ç", "-"]
spacingChars = [";",".",",","!","?","%","$","#",":"]

pronounsAndArticles = ["I","me","my","mine","myself","you","your","yours","yourself","he","him","his","himself","she",
                       "her","her","hers","herself","it","its","itself","we","us","our","ours","ourselves","you","your",
                       "yours","yourselves","they","them","their","theirs","themselves", "and", "the", "for", "with"]

pronomsEtDet = ["je", "me", "m’", "moi", "tu", "te", "t’", "toi", "nous","il", "elle", "ils", "elles","se",
                "en","y","le", "la", "l’", "les", "lui", "soi", "leur", "eux","lui", "leur", "des", "aux", "au","mes", "qui", "avec", "sur","à", "un", "une", " dans","que", "mes","mon","ton"]
plurialFormList = ["s", "x"]

GlobalDict ={}

class Main:
    def Naive(self, file):
        Training()
        result = Training.Result(self, file)
        return result

class Training:
    def __init__(self):
        global Path, NbPositive, NbNegative
        parsingText = TextParser()


        ##
        #rejected and accepted paths
        ##
        pathAccepted = r"\Adjointes\Apprentissage\Engagés"
        pathRejected = r"\Adjointes\Apprentissage\Rejetés"

        acceptedNames = glob2.glob(Path + pathAccepted + "\*.docx")
        rejectedNames = glob2.glob(Path + pathRejected + "\*.docx")

        negativeWords = []
        positiveWords = []
        for x in range(0, len(acceptedNames)):
            positiveWords += parsingText.textParser(acceptedNames[x])
        for x in range(0, len(rejectedNames)):
            negativeWords += parsingText.textParser(rejectedNames[x])

        positiveDict = {}
        negativeDict = {}

        # training section, code is training algorithm based on positve and negative samples and will later combine the results to a global dictionnary in order to make predictions on futur CVs

        for x in range(0, len(positiveWords)):
            word = None
            if positiveDict.get(positiveWords[x]) is None:   # ce n'est pas is None?
                positiveDict[positiveWords[x]] = WordsData(positiveWords[x], 1, 0, nBOfAppearances=1)
            else:
                word = positiveDict.get(positiveWords[x])
                word.Positivity += 1
                word.NBOfAppearances +=1
        NbPositive = len(positiveWords)

        for x in range(0, len(negativeWords)):
            word = None
            if negativeDict.get(negativeWords[x]) == None:
                negativeDict[negativeWords[x]] = WordsData(negativeWords[x], 0, 1, nBOfAppearances=1)
            else:
                word = negativeDict.get(negativeWords[x])
                word.Negativity += 1
                word.NBOfAppearances +=1

        NbNegative = len(negativeWords)



        for x in range(0, len(positiveWords)):
            word = None
            if negativeDict.get(positiveWords[x]) == None:
                negativeDict[positiveWords[x]] = positiveDict[positiveWords[x]]
            else:
                negativeDict[positiveWords[x]].Positivity = positiveDict[positiveWords[x]].Positivity

                negativeDict[positiveWords[x]].NBOfAppearances += 1




        dictOfWords = negativeDict

        plurialsToRemove = []
        for words in dictOfWords:
            if BayesClassifier.PlurialForm(self, words, dictOfWords) != words:
                parentWord = BayesClassifier.PlurialForm(self, words, dictOfWords)
                dictOfWords.get(parentWord).Positivity = dictOfWords.get(words).Positivity
                dictOfWords.get(parentWord).Negativity = dictOfWords.get(words).Negativity
                dictOfWords.get(parentWord).ProbabilityOfPositive = dictOfWords.get(words).ProbabilityOfPositive
                dictOfWords.get(parentWord).NBOfAppearances = dictOfWords.get(words).NBOfAppearances
                plurialsToRemove.append(words)

        for word in plurialsToRemove:
            del dictOfWords[word]



        #for words in dictOfWords:
         #   print("-------------------------")
          #  print(dictOfWords[words].Word)
           # print(dictOfWords[words].NBOfAppearances)
            #print(dictOfWords[words].Positivity)
            #print(dictOfWords[words].Negativity)


        BayesClassifier.Training(self, dictOfWords)

    def Result(self, file):

        ##
        #getting the CV to evaluate
        ##
        parsingText = TextParser()
        pathAcceptedTest = r"\Adjointes\Test\Engagés"
        pathRejectedTest = r"\Adjointes\Test\Rejetés"

        candidat = r"\adjointe  Emmanuella_Douillard.docx"

        import os
        ...
#        yes =0
#        no = 0
#        totalyYes =0
#        totalNo = 0
#        for filename in os.listdir(Path + pathAcceptedTest):
#            #filename.
#            specificList = parsingText.textParser(Path + pathAcceptedTest + "\\" +filename)
#           # print(specificList)
#            specificDict = {}
#            for x in range(0, len(specificList)):
#                word = None
#                if specificDict.get(specificList[x]) == None:
#                    specificDict[specificList[x]] = WordsData(specificList[x], 1, 0)
#                else:
#                    word = specificDict.get(specificList[x])
#
#
#           # print(" here " + str(specificDict))
#
#            result = BayesClassifier.CompareToGeneralDictionnary(self, specificDict)
#            if result == True:
#                yes+=1
#            totalyYes=len(os.listdir(Path + pathRejectedTest))
#
#        print('#####################################################')
#        print('#####################################################')
#        print('#####################################################')
#        for filename in os.listdir(Path + pathRejectedTest):
#            #filename.
#            specificList = parsingText.textParser(Path + pathRejectedTest + "\\" +filename)
#           # print(specificList)
#            specificDict = {}
#            for x in range(0, len(specificList)):
#                word = None
#                if specificDict.get(specificList[x]) == None:
#                    specificDict[specificList[x]] = WordsData(specificList[x], 1, 0)
#                else:
#                    word = specificDict.get(specificList[x])
#
#
#           # print(" here " + str(specificDict))
#
#            result = BayesClassifier.CompareToGeneralDictionnary(self, specificDict)
#            if result == False:
#                no+=1
#            totalNo=len(os.listdir(Path + pathRejectedTest))
        ...
        specificList =  parsingText.textParser(file)
       # print(specificList)
        specificDict = {}
        for x in range(0, len(specificList)):
            word = None
            if specificDict.get(specificList[x]) == None:
                specificDict[specificList[x]] = WordsData(specificList[x], 1, 0)
            else:
                word = specificDict.get(specificList[x])


       # print(" here " + str(specificDict))

        result = BayesClassifier.CompareToGeneralDictionnary(self, specificDict)
        #print (str(result) + " personnal result")

        #print (str(yes/totalyYes) + " result %")
        #print (str(no/totalNo) + " result %")
        return result


class BayesClassifier:
    def Training(self, dictOfWords):
        global GlobalDict
        for word in dictOfWords:
            wordObject = dictOfWords[word]
            probabilityOfPositive = BayesClassifier.individualProbs(self, wordObject)
            wordObject.ProbabilityOfPositive = probabilityOfPositive

        GlobalDict = dictOfWords



    def individualProbs(self, word):
        global NbPositive, NbNegative
        totalCV = NbPositive + NbNegative

        priorProbabilityOfPositive = NbPositive / totalCV
        priorProbabilityOfNegative = NbNegative / totalCV

        probabilityOfPositive = 0
        if word.Positivity + word.Negativity != 1:

            probabilityOfPositive = (word.Positivity/(word.Positivity + word.Negativity))
            print(probabilityOfPositive)
        return probabilityOfPositive



    def CombiningProbs(self, dictOfWords, positiveDictCount, negativeDictCount):
        global NbPositive, NbNegative

        totalCV = NbPositive + NbNegative
        #totalPositiveWords = len(positiveDict)

        #totalNegativeWords = len(negativeDict)


        totalWords = positiveDictCount + negativeDictCount
        priorProbabilityOfPositive = positiveDictCount / totalWords
        priorProbabilityOfNegative = negativeDictCount / totalWords
        print('#####################################################')
        print(totalWords)
        #print(priorProbabilityOfPositive)
        #print(priorProbabilityOfNegative)
        print('#####################################################')
        #  priorProbabilityOfPositive = NbPositive / totalCV
        #  priorProbabilityOfNegative = NbNegative / totalCV


        probabilityOfPositive = 100
        probabilityOfNegative = 100


        # test
        positivity = 0
        total = 0
        #
        for wordKey in dictOfWords:
            #wordObject = dictOfWords[wordKey]

            if(wordKey.ProbabilityOfPositive >(.5*priorProbabilityOfPositive)/ priorProbabilityOfNegative):
                positivity+=1
            total +=1
            probabilityOfPositive *= wordKey.ProbabilityOfPositive

            probabilityOfNegative *= (1-wordKey.ProbabilityOfPositive)

            print("Word : " + str(wordKey.Word)+ ", word probability : "+ str(wordKey.ProbabilityOfPositive)
                  +", probabilityOfPositive : " + str(probabilityOfPositive) + ", probabilityOfNegative : "
                  + str(probabilityOfNegative) + ", word seeage : " + str(wordKey.NBOfAppearances))

        evidence = probabilityOfPositive * priorProbabilityOfPositive + probabilityOfNegative * priorProbabilityOfNegative
        #print(str(positivity) + " " + str(total) + " " + str((.5*priorProbabilityOfPositive)/ priorProbabilityOfNegative))
        #result = positivity/total
        #print(result)

        probabilityOfPositive *= priorProbabilityOfPositive
        probabilityOfNegative *= priorProbabilityOfNegative


        probabilityOfPositive /= evidence
        probabilityOfNegative /= evidence

        print(probabilityOfPositive*100)
        print(probabilityOfNegative*100)
        return (probabilityOfPositive*100)
        #if probabilityOfPositive > probabilityOfNegative:
        #    return True
        #    print("yes")
        #else:
        #    return False
         #   print("no")

    def PlurialForm(self, string, GlobalDict):

        for word in GlobalDict:
            if len(word)+1 == len(string):
                totalCheck = 0
                for x in range(0, len(word)):
                    if word[x] == string[x]:
                        totalCheck+=1
                if totalCheck == len(word):
                    if string[-1] in plurialFormList:
                        return word
        return string




    def CompareToGeneralDictionnary(self, specificDict):
        global GlobalDict
        wordsToRemove = []
        finalDict = {}

        for word in specificDict:
            if GlobalDict.get(word) != None:
                wordObject = GlobalDict[word]
                if wordObject.ProbabilityOfPositive > .2 and wordObject.ProbabilityOfPositive < .8:
                    finalDict[wordObject] = wordObject
                    #print(wordObject.Word)
                    #print(specificDict[word].Positivity)
                else:
                    wordsToRemove.append(word)
        positiveWordCount = 0
        negativeWordCount = 0
        for words in finalDict:
            positiveWordCount += words.Positivity
            negativeWordCount += words.Negativity


        for words in wordsToRemove:
            del specificDict[words]


        finalDict = BayesClassifier.SuppCriterias(self, finalDict)


        #print(finalDict.keys())
        result = BayesClassifier.CombiningProbs(self, finalDict, positiveWordCount, negativeWordCount)
        return result

    def SuppCriterias(self, dict):
        ##
        dict = BayesClassifier.RemoveTooLowReccurences(self, dict, 10)
        ##
        dict = BayesClassifier.RemovePronouns(self, dict)
        ##
        dict = BayesClassifier.RemoveLowCharCounts(self, dict, 5)
        ##
        return dict

    def RemoveTooLowReccurences(self, dict, amount):
        newDict = {}
        for word in dict:
            if dict.get(word) != None:
                wordObject = dict[word]
                if wordObject.NBOfAppearances > amount:
                    newDict[wordObject] = wordObject

        return newDict

    def RemovePronouns(self, dict):
        global pronounsAndArticles, pronomsEtDet
        newDict = {}
        for word in dict:
            if dict.get(word) != None:
                wordObject = dict[word]
                if wordObject.Word not in pronounsAndArticles and wordObject.Word not in pronomsEtDet:
                    newDict[wordObject] = wordObject

        return newDict

    def RemoveLowCharCounts(self, dict, amount):
        global spacingChars
        newDict = {}
        for word in dict:
            if dict.get(word) != None:
                wordObject = dict[word]
                if wordObject.Word in spacingChars == True or len(wordObject.Word) > amount:
                    newDict[wordObject] = wordObject

        return newDict

class TextParser:
    def textParser(self, nameOfFile):
        global Path

        firstDraft = self.OpenText(nameOfFile)
        secondDraft = self.AcceptableCharsFND(firstDraft)
        thidDraft = self.ProperSpacing(secondDraft)
        fourthDraft = self.RemoveWhiteSpace(thidDraft)
        fifthDraft = fourthDraft.split()
        #print("fifth " + str(fifthDraft))
        return fifthDraft

    def OpenText(self, nameOfFile):
        file = docx.Document(nameOfFile)
        firstDraft = [p.text for p in file.paragraphs]
        return firstDraft

    def AcceptableCharsFND(self, firstDraft):
        secondDraft = ""
        secondArray = []
        for x in range(0, len(firstDraft)):
            secondDraft = ""
            for y in range(0, len(firstDraft[x])):
                if firstDraft[x][y].lower() in acceptableChars or firstDraft[x][y].lower() in spacingChars:
                    secondDraft += firstDraft[x][y].lower()
                else:
                    secondDraft += " "
            secondArray.append(secondDraft)
        return secondArray

    def ProperSpacing(self, stringList):
        thirdDraft = ""
        for string in stringList:
            x = 1
            max = len(string)


            while(x < max):

                if string[x] in spacingChars:
                    string = string[:x] + " " + string[x] + " " + string[x+1:]
                    max+=2
                    x+=1
                x+=1
            thirdDraft+= string + " "
        return thirdDraft

    def RemoveWhiteSpace(self, string):
        stringReturn = " ".join(string.split())
        return stringReturn

class WordsData:
    Word = ""
    Positivity = 0
    Negativity = 0
    ProbabilityOfPositive = 0
    NBOfAppearances = 0
    def __init__(self, word, positivity = 0, negativity = 0, probabilityOfPositive = 0, nBOfAppearances = 0):
        self.Word = word
        self.Positivity = positivity
        self.Negativity = negativity
        self.ProbabilityOfPositive = probabilityOfPositive
        self.NBOfAppearances = nBOfAppearances



if __name__ == '__main__':
    main = Main()
    main.Naive()
