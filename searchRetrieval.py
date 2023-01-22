# Name - Tejas Dhananjay Rajopadhye
# UIN - 675873639
# CS 582 Final Project
# Please take a look at Project report for more information on this file and the usage for the same
## ***** Please supply three input args
## 1 - Input path to the input HTML Documents file directory (e.g. - c:\users\RetrivedDocs\ )

import json
import math
from pathlib import Path
from bs4 import BeautifulSoup
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import argparse

"""
Funtion to extract the XML tag data from the SGML document
"""
def extractTextFromXML(XMldoc, tagLabel):
    xmlDataLocal = BeautifulSoup(XMldoc)
    return xmlDataLocal.find(tagLabel).string

"""
Function to process text - The processing happens as described in the HW2 description
"""
def textProcessing(text):
    text = text.lower()

    ## Remove the \n's from the text
    text = text.replace('\n', " ")

    ## Remove the punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    ## Remove numbers
    text = text.translate(str.maketrans('', '', string.digits))

    ## Remove the stop words
    arrOfTokens = text.split()
    arrProcessed = []
    stop_words = set(stopwords.words('english'))
    for wordToken in arrOfTokens:
        if (wordToken not in stop_words):
            arrProcessed.append(wordToken)
    arrOfTokens = arrProcessed

    ## Perform Stemming
    porterStemmerObj = PorterStemmer()
    arrayOfTokensWithStemming = []
    for wordToken in arrOfTokens:
        arrayOfTokensWithStemming.append(porterStemmerObj.stem(wordToken))
    arrOfTokens = arrayOfTokensWithStemming

    ## Again Remove the stop words
    arrProcessed = []
    for wordToken in arrOfTokens:
        if (wordToken not in stop_words):
            arrProcessed.append(wordToken)
    arrOfTokens = arrProcessed

    ## Join the string together
    text = ' '.join(map(str, arrOfTokens))

    ## Remove words of some length
    text = re.compile(r'\W*\b\w{1,2}\b').sub('', text)

    processedText = text
    return processedText

"""
Generate the TF ( word Frequency ) for a given text string
"""
def getTF(text):
    wordDict = dict()
    text = text.split()
    for token in text:
        if token in wordDict:
            wordDict[token] = wordDict[token] + 1
        else:
            wordDict[token] = 1
    return wordDict

"""
Generate the DF data for all docs 
This function takes all docs dictionary and iterates over all the documents strings and constructs inverted index 
This inverted index is used to construct DF dictionary for all documents 
"""
def getDFFromAllDocs(allDocsDict):
    dfDict = dict()
    intDict = dict()  #Intermediate dictionary
    for doc in allDocsDict:
        textFromDoc = allDocsDict[doc]
        #Create a Inverted Index
        tokens = textFromDoc.split()
        for token in tokens:
            if token in intDict:
                if doc not in intDict[token]:
                    intDict[token].append(doc)
            else:
                intDict[token] = [doc]

    for dictVal in intDict:
        dfDict[dictVal] = len(intDict[dictVal])
    return dfDict

"""
Function to generate tf-idf data from the doc 
This function takes input doc ( string ), dfDict ( generated with getDFFromAllDocs ) , total number of docs
Calculates the tf-idf from the documents  
"""
def generatetfIdfFromDoc(doc, dfDict, numOfDocs):
    tfDict = getTF(doc)
    words = doc.split()
    tfIdfDict = dict()
    for word in words:
        ## Adding + 1 to get rid of divide by zero errors
        tfIdfDict[word] = tfDict[word] * math.log2(numOfDocs / dfDict[word] + 1)
    return tfIdfDict

"""
Calculate the cosine similarity 
This function takes the docVec which is a dictioary of { word : tf-idf } values. queryVec is a similar dict 
For each word in query , if this word exist in the docVec the multiplication is made and the sum is accumulated
getNorm function calculated the denominator
"""
def getCosineSim(docVec, queryVec):
    numerator = 0.0
    for qDictVal in queryVec:
        if qDictVal in docVec:
            numerator = numerator + queryVec[qDictVal] * docVec[qDictVal]

    docNorm = getNorm(docVec)
    queryNorm = getNorm(queryVec)

    return (numerator / math.sqrt(docNorm * queryNorm + 1))


"""
Calculate the norm of a dictionary vector 
"""
def getNorm(dicVec):
    value=0.0
    for vec in dicVec:
        value = dicVec[vec] * dicVec[vec]
    return value

"""
Function to calculate the cosine similarities between all docs and query docs
Return dict of doc to query cosine similarity for all docs and a given query 
"""
def calculateCosineVec(allTfIdfDoc, queryIdfDoc):
    docToQuerySim = dict()
    for docTfIdf in allTfIdfDoc:
        docToQuerySim[docTfIdf] = getCosineSim(allTfIdfDoc[docTfIdf], queryIdfDoc)
    return docToQuerySim

"""
Generate the (query_id, document_id) output from the cosine documents
This function takes the cosine similarities generated for all the documents 
Later in the code convert it to the {query_id : rankedDoc_dict} . This represenation is useful to calculate the recall and precision. Please check the generate output function for the same 
"""
def getQueryIdDocId(cosSineQueriesDoc):
    arrayOfQueryIdDocId = []
    outputDict = dict()
    for cosDicVal in cosSineQueriesDoc:
        docDict = cosSineQueriesDoc[cosDicVal]
        #Sort it based on the cosine sim
        docDict = dict(sorted(docDict.items(), key=lambda data: data[1], reverse=True))
        for docDicVals in docDict:
            arrayOfQueryIdDocId.append([str(cosDicVal), docDicVals])
        outputDict[cosDicVal] = arrayOfQueryIdDocId
        arrayOfQueryIdDocId = []
    return outputDict

"""
Find the ranked docs which match the relevance doc answers
This function finds the intersection between the relevant data and the docs ranked that are generated with cosine similarity
"""
def findCommanDocs(docRanked, relevantDocRanked):
    numOfCommonDocs = 0
    for doc in docRanked:
        if doc in relevantDocRanked:
            numOfCommonDocs = numOfCommonDocs + 1
    return numOfCommonDocs


"""
Get the conversion from the queryDoc dict to a queryURL to display the links searched by the query doc 
"""
def getQueryURLDoc(queryDocId, mapDocToURL):
    queryURLDoc = dict()
    for query in queryDocId:
        queryURLDoc[query] = list()
        for element in queryDocId[query]:
            queryURLDoc[query].append(mapDocToURL[element[1]])
    return queryURLDoc

def startSearchTerminal():
    while(1):
        print("**** Enter the string to search ****")
        print("** Type -1 to exit the search engine")
        searchText = input("Enter the string now ...")

        if (searchText == str(-1)):
            return
        queriesDoc = list()
        queriesDoc.append(searchText)
        queriesDict = dict()
        for queryIndex in range(len(queriesDoc)):
            queriesDict[queryIndex + 1] = textProcessing(queriesDoc[queryIndex])

        ## Calculate the tfidf for the queries
        queriesDocTfIdfDict = dict()
        dfDictForQueries = getDFFromAllDocs(queriesDict)
        for doc in queriesDict:
            # dictVal = generatetfIdfFromDoc(queriesDict[doc], dfDictForQueries, len(queriesDoc))
            dictVal = generatetfIdfFromDoc(queriesDict[doc], dfDictForQueries, numOfDocs)
            queriesDocTfIdfDict[doc] = dictVal

        ## Now find cosine similarity between the queries and the docs
        cosSineQueriesDoc = dict()

        ## Generate CosineSim
        for qDoc in queriesDocTfIdfDict:
            cosSineQueriesDoc[qDoc] = calculateCosineVec(allDocsTfIdf, queriesDocTfIdfDict[qDoc])

        ## Now generate the (queryId, documentId) combination
        queryIdDocId = getQueryIdDocId(cosSineQueriesDoc)

        # Load the MapDocToURL
        mapDocToURLFile = open("./mapDocToURL", "r")
        readFiled = mapDocToURLFile.read()
        mapDocToURL = json.loads(readFiled)
        queryURLDoc = getQueryURLDoc(queryIdDocId, mapDocToURL)

        count = 10

        while(1):
            #for inst in queryURLDoc:
            #print("Document Retrieved for query - > " + str())
            printURLSearched(queryURLDoc, 1, count)
            print("----------------------")
            moreRecords = input("Press 1 for more records OR press 0 for exiting OR -1 to search more")
            if(moreRecords == str(0)):
                return
            if (moreRecords == str(-1)):
                break
            count = count + 10

def printURLSearched(queryURLDoc, inst, count):
    for itr in range(0, count):
        print(queryURLDoc[inst][itr])

## Main Entry point
if __name__ == '__main__':
    # Args Configuration
    parser = argparse.ArgumentParser(description='Args to Search Terminal For Final Project')
    parser.add_argument('HTMLDocs', type=str,
                        help='Please specify a correct input path to the Retrieved HTML Docs')

    args = parser.parse_args()
    path = args.HTMLDocs

    # Hold Text Data for all Docs in a hashmap
    allDocsTextDict = dict()
    numOfDocs = 0
    # Iterate Over all Files and Make a Text
    fileEntries = Path(path)
    for fileEntry in fileEntries.iterdir():
        fileR = open(path + "/" + fileEntry.name, mode='r', encoding='utf-8')
        textWithoutProcessing = fileR.read()
        # Now process this string and tokenize
        textAfterProcessing = textProcessing(textWithoutProcessing)
        allDocsTextDict[fileEntry.name] = textAfterProcessing
        numOfDocs = numOfDocs + 1

    ## Function call to generate the DF For all docs
    dfDict = getDFFromAllDocs(allDocsTextDict)

    ## Calculate the tfidf values for all doc
    allDocsTfIdf = dict()
    for doc in allDocsTextDict:
        dictVal = generatetfIdfFromDoc(allDocsTextDict[doc], dfDict, numOfDocs)
        allDocsTfIdf[doc] = dictVal

    startSearchTerminal()

