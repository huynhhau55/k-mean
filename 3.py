import csv
import sys
import math
import random
import matplotlib.pyplot as plt
import numpy

ignoreAttributeIndex = [1, 2, 5, 6, 8, 10, 12, 12]
usedAttrNum = 6
class Cluster(object):
    def __init__(self, centroid):
        self.centroid = centroid
        self.members = []

    def addEntry(self, entry):
        self.members.append(entry)
    def changeCentroid(self, centroid):
        self.centroid = centroid
    def printOut(self):
        print("centroid:")
        print(self.centroid)
        print("members:")
        print(self.members)
    def getWCScore(self, isManhattan):
        score = 0
        for entry in self.members:
            dist = distance(self.centroid, entry, isManhattan)
            dist = math.pow(dist, 2)
            score += dist
        return score

def connectToClusters(dataset, clusters, isManhattan):
    print("Connect to clusters--------------------------------------------")
    for entry in dataset:
        minDistance = 9999999.99
        resultCentroidIndex = 0
        for index, cluster in enumerate(clusters):
            dist = distance(cluster.centroid, entry, isManhattan)
            if ( dist < minDistance ):
                minDistance = dist
                resultCentroidIndex = index
        clusters[resultCentroidIndex].addEntry(entry)
    print(clusters)
def changeClustersWithData(clusters):
    print("\nchangeClustersWithData++++++++++++++++++++++++++++++++++++++++")
    
    for idx, cluster in enumerate(clusters):
        print(clusters[2].members)
        newMeanCentroid = []
        for i in range(usedAttrNum):
            newMeanCentroid.append(0)
        for entry in cluster.members:
            for index, val in enumerate(entry):
                newMeanCentroid[index] += val/len(cluster.members)
        clusters[idx].changeCentroid(newMeanCentroid)

def changeMembersWithNewClusters(clusters, isManhattan):
    numOfChanges = 0
    for mainIndex, mainCluster in enumerate(clusters):
        for entry in mainCluster.members:
            currentDistance = distance(mainCluster.centroid, entry, isManhattan)
            minDistance = currentDistance
            resultClusterIndex = mainIndex
            for subIndex, subCluster in enumerate(clusters):
                dist = distance(subCluster.centroid, entry, isManhattan)
                if dist < minDistance:
                    minDistance = dist
                    resultClusterIndex = subIndex
            if resultClusterIndex != mainIndex:
                mainCluster.members.remove(entry)
                clusters[resultClusterIndex].members.append(entry)
                numOfChanges += 1
    return numOfChanges

def distance(first, second, isManhattan):
    # print("Run distance function for caculating the distance+++++++++++++++++++++++++++++++")
    # print(first)
    # print(second)
    print("Dang tinh distance.....")
    result = 0
    if isManhattan:
        for index, val in enumerate(first):
            result += val - second[index]
    else:
        sum = 0
        for index, val in enumerate(first):
            sum += math.pow(val-second[index], 2)
        result = math.sqrt(sum)
    return result

def read_arff(inputFile):
    resultArr = []
    headers = []
    data = []
    f = open(inputFile, "r")
    contents = f.read()
    file_as_list = contents.splitlines()
    handle_converting_csv(file_as_list, headers, data)
    resultData = data
    #age, blood-pressure, cholesterol, maximum-heart-rate, peak, colored-vessels
    entryLength = len(data[0])
    for i in range(len(data)):
        for index in sorted(ignoreAttributeIndex, reverse=True):
            data[i].pop(index)
        for index, val in enumerate(data[i]):
            resultData[i][index] = float(val)
    
    # print("Result: ")
    # print(resultArr)
    # print("headers: ")
    # print(headers)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++data: ")
    print(resultData)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    return resultArr, headers, resultData

def handle_converting_csv(arffDataList, headers, data):
    readForData = False
    for line in arffDataList:
        lineList = line.split(" ")
        if len(lineList) == 0:
            continue
        if readForData == True and lineList[0] != '%':
            data.append(lineList[0].split(","))
        if lineList[0] == '@attribute':
            headers.append(lineList[1].replace("'", ''))
        if lineList[0] == '@data':
            readForData = True

def generateRandomCentroids(dataset, k):
    print("Generate random centroids-------")
    points = random.sample(dataset, k)
    clusters = []
    for centroid in points:
        cluster = Cluster(centroid)
        clusters.append(cluster)
    print("Clusters: ")
    for c in clusters:
        c.printOut()
    return clusters

def main():
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    kNumber = int(sys.argv[3])
    print(sys.argv)

    # inputFile = "cardiology-cleaned.arff"
    # kNumber = 3
    # outputFile = "abc.txt"

    resultArr, headers, data = read_arff(inputFile)

    clusters = generateRandomCentroids(data, kNumber)


    for e in enumerate(clusters):
        print(e)
    #thuNghiemXuLy
    isManhattan = False
    connectToClusters(data, clusters, isManhattan)
    changeClustersWithData(clusters)
    while changeMembersWithNewClusters(clusters, isManhattan) != 0:
        changeClustersWithData(clusters)
    totalScore = 0
    output = open(str(kNumber)+"-"+outputFile, "w")
    for index, cluster in enumerate(clusters):
        totalScore += cluster.getWCScore(isManhattan)
    print("WC-SSE=" + str(totalScore))
    output.write("WC-SSE=" + str(totalScore) + "\n")
    for index, cluster in enumerate(clusters):
        print("Centroid" + str(index + 1) + "=" + str(cluster.centroid))
        output.write("Centroid" + str(index + 1) + "=" + str(cluster.centroid) + "\n")
    output.close()

#Example: python 3.py cardiology-cleaned.arff clusters.txt 3
main()