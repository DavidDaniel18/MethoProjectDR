import docx
import glob2
import math

NbPositive = 0
NbNegative = 0

Path = r"C:\Users\david\OneDrive\Documents\ProjetRobertoDavid\DataSet"
acceptableChars = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
                   "é", "è", "à", "û", "ô", "'", "d'","ç"]
spacingChars = [";",".",",","!","?","%","$","#",":"]

pronounsAndArticles = ["I","me","my","mine","myself","you","your","yours","yourself","he","him","his","himself","she",
                       "her","her","hers","herself","it","its","itself","we","us","our","ours","ourselves","you","your",
                       "yours","yourselves","they","them","their","theirs","themselves"]

pronomsEtDet = ["je", "me", "m’", "moi", "tu", "te", "t’", "toi", "nous", "vous","il", "elle", "ils", "elles","se",
                "en","y","le", "la", "l’", "les", "lui", "soi", "leur", "eux","lui", "leur", "des"]

GlobalDict ={}

class Main:
    def Naive(self):
        Training()

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

        for x in range(0, len(positiveWords)):
            word = None
            if positiveDict.get(positiveWords[x]) == None:
                positiveDict[positiveWords[x]] = WordsData(positiveWords[x], 1, 0, nBOfAppearances=1)
            else:
                word = positiveDict.get(positiveWords[x])
                word.Positivity += 1
                word.NBOfAppearances +=1
        NbPositive = len(positiveWords)

        for x in range(0, len(negativeWords)):
            word = None
            if negativeDict.get(negativeWords[x]) == None:
                negativeDict[negativeWords[x]] = WordsData(negativeWords[x], 0, 1 , nBOfAppearances=1)
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

        #for words in dictOfWords:
         #   print("-------------------------")
          #  print(dictOfWords[words].Word)
           # print(dictOfWords[words].NBOfAppearances)
            #print(dictOfWords[words].Positivity)
            #print(dictOfWords[words].Negativity)


        BayesClassifier.Training(self, dictOfWords)



        ##
        #getting the CV to evaluate
        ##
        pathAcceptedTest = r"\Adjointes\Test\Engagés"
        pathRejectedTest = r"\Adjointes\Test\Rejetés"

        candidat = r"\Virginie_DOREet assurance vie. - Copie.docx"

        specificList = parsingText.textParser(Path + pathAcceptedTest + candidat)
        specificDict = {}
        for x in range(0, len(specificList)):
            word = None
            if specificDict.get(specificList[x]) == None:
                specificDict[specificList[x]] = WordsData(specificList[x], 1, 0)
            else:
                word = specificDict.get(specificList[x])



        BayesClassifier.CompareToGeneralDictionnary(self, specificDict)




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

    def CombiningProbs(self, dictOfWords):
        global NbPositive, NbNegative

        totalCV = NbPositive + NbNegative

        priorProbabilityOfPositive = NbPositive / totalCV
        priorProbabilityOfNegative = NbNegative / totalCV


        probabilityOfPositive = 100
        probabilityOfNegative = 100

        for wordKey in dictOfWords:
            #wordObject = dictOfWords[wordKey]
            probabilityOfPositive *= wordKey.ProbabilityOfPositive

            probabilityOfNegative *= (1-wordKey.ProbabilityOfPositive)

            print("Word : " + str(wordKey.Word)+ ", word probability : "+ str(wordKey.ProbabilityOfPositive)
                  +", probabilityOfPositive : " + str(probabilityOfPositive) + ", probabilityOfNegative : "
                  + str(probabilityOfNegative) + ", word seeage : " + str(wordKey.NBOfAppearances))

        evidence = probabilityOfPositive * priorProbabilityOfPositive + probabilityOfNegative * priorProbabilityOfNegative



        probabilityOfPositive *= priorProbabilityOfPositive
        probabilityOfNegative *= priorProbabilityOfNegative


        probabilityOfPositive /= evidence
        probabilityOfNegative /= evidence

        print(probabilityOfPositive*100)
        print(probabilityOfNegative*100)

        if probabilityOfPositive > probabilityOfNegative:
            print("yes")
        else:
            print("no")

    def CompareToGeneralDictionnary(self, specificDict):
        global GlobalDict
        wordsToRemove = []
        finalDict = {}
        for word in specificDict:
            if GlobalDict.get(word) != None:
                wordObject = GlobalDict[word]
                if wordObject.ProbabilityOfPositive > .1 and wordObject.ProbabilityOfPositive < .9:
                    finalDict[wordObject] = wordObject
                    #print(wordObject.Word)
                    #print(specificDict[word].Positivity)
                else:
                    wordsToRemove.append(word)


        for words in wordsToRemove:
            del specificDict[words]
        finalDict = BayesClassifier.SuppCriterias(self, finalDict)
        BayesClassifier.CombiningProbs(self, finalDict)

    def SuppCriterias(self, dict):
        ##
        #dict = BayesClassifier.RemoveTooLowReccurences(self, dict, 4)
        ##
        #dict = BayesClassifier.RemovePronouns(self, dict)
        ##
        #dict = BayesClassifier.RemoveLowCharCounts(self, dict, 2)
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
                if wordObject.Word not in pronounsAndArticles and wordObject.Word not in  pronomsEtDet :
                    newDict[wordObject] = wordObject

        return newDict

    def RemoveLowCharCounts(self, dict, amount):
        global spacingChars
        newDict = {}
        for word in dict:
            if dict.get(word) != None:
                wordObject = dict[word]
                if wordObject.Word in  spacingChars == True or len(wordObject.Word) > amount:
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
        return fifthDraft

    def OpenText(self, nameOfFile):
        file = docx.Document(nameOfFile)
        firstDraft = [p.text for p in file.paragraphs]
        return firstDraft

    def AcceptableCharsFND(self, firstDraft):
        secondDraft = ""
        for x in range(0, len(firstDraft)):
            for y in range(0, len(firstDraft[x])):
                if firstDraft[x][y].lower() in acceptableChars or firstDraft[x][y].lower() in spacingChars:
                    secondDraft += firstDraft[x][y].lower()
                else:
                    secondDraft += " "

        return secondDraft

    def ProperSpacing(self, string):
        x = 1
        max = len(string)


        while(x < max):

            if string[x] in spacingChars:
                string = string[:x] + " " + string[x] + " " + string[x+1:]
                max+=2
                x+=1
            x+=1

        return string

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
