_author_ = 'thanakorn suppakarnpanich'

import sys
import itertools
import random
import copy
import math


def runPrediction():
    k = int(sys.argv[len(sys.argv)-1])
    userAndMovieString = ''
    flag = 0
    for i in range(2, len(sys.argv)-1):
        if flag == 0:
            userAndMovieString += sys.argv[i]
            flag = 1
        else:
            userAndMovieString += " " + sys.argv[i]
    userAndMovieArray = userAndMovieString.split("\'")
    userId = userAndMovieArray[1]
    movie = userAndMovieArray[3]
    neighbors = k_nearest_neighbors(userId, k)
    for each in neighbors:
        print each[0] + " " + str(each[1])
    print str(predict(userId, movie, neighbors))


def pearson_correlation(user1, user2):
    fileName = sys.argv[1]
    inFile = open(fileName, 'r')
    user1Dictionary = {}
    user2Dictionary = {}
    for line in inFile:
        line = line.replace("\n", "")
        ratingArray = line.split("\t")
        if ratingArray[0] == user1:
            user1Dictionary[ratingArray[2]] = float(ratingArray[1])
        elif ratingArray[0] == user2:
            user2Dictionary[ratingArray[2]] = float(ratingArray[1])
    user1Keys = set(user1Dictionary.keys())
    user2Keys = set(user2Dictionary.keys())
    intersection = user1Keys & user2Keys
    user1Sum = 0
    user2Sum = 0
    for key in intersection:
        user1Sum += user1Dictionary[key]
        user2Sum += user2Dictionary[key]
    user1Average = user1Sum/len(intersection)
    user2Average = user2Sum/len(intersection)
    nominator = 0;
    user1Denominator = 0;
    user2Denominator = 0;
    for key in intersection:
        nominator += (user1Dictionary[key] - user1Average) * (user2Dictionary[key] - user2Average)
        user1Denominator += math.pow((user1Dictionary[key] - user1Average), 2)
        user2Denominator += math.pow((user2Dictionary[key] - user2Average), 2)
    user1Denominator = math.sqrt(user1Denominator)
    user2Denominator = math.sqrt(user2Denominator)
    weight = nominator/(user1Denominator*user2Denominator)
    return weight

def k_nearest_neighbors(user1, k):
    fileName = sys.argv[1]
    inFile = open(fileName, 'r')
    userKeySet = set()
    for line in inFile:
        ratingArray = line.split("\t")
        if ratingArray[0] != user1:
            userKeySet.add(ratingArray[0])
    neighborsArray = []
    for key in userKeySet:
        similarity = pearson_correlation(user1, key)
        neighborsArray.append((key, similarity))
    neighborsArray.sort(key=lambda x: x[0])
    neighborsArray.sort(key=lambda x: x[1], reverse=True)
    resultList = []
    for i in range(0, k):
        resultList.append(neighborsArray[i])
    return resultList


def predict(user1, item, k_nearest_neighbors):
    fileName = sys.argv[1]
    inFile = open(fileName, 'r')
    neighborDictionary = {}
    user1Average = 0
    user1Sum = 0
    user1Count = 0
    user1Keys = set()
    for line in inFile:
        line = line.replace("\n", "")
        ratingArray = line.split("\t")
        for neighbor in k_nearest_neighbors:
            if ratingArray[0] == neighbor[0]:
                if ratingArray[0] in neighborDictionary:
                    neighborDictionary[ratingArray[0]].append((ratingArray[2], float(ratingArray[1])))
                else:
                    ratingList = [(ratingArray[2], float(ratingArray[1]))]
                    neighborDictionary[ratingArray[0]] = ratingList
        if ratingArray[0] == user1:
            user1Keys.add(ratingArray[2])
            user1Sum += float(ratingArray[1])
            user1Count += 1
    user1Average = user1Sum/user1Count
    filteredNeighborsDictionary = {}
    for key, value in neighborDictionary.iteritems():
        for rating in value:
            if rating[0] == item:
                filteredNeighborsDictionary[key] = value
    nominator = 0
    denominator = 0
    for key, value in filteredNeighborsDictionary.iteritems():
        sumValue = 0
        count = 0
        itemRate = 0
        for rating in value:
            if rating[0] != item:
                if rating[0] in user1Keys:
                    sumValue += rating[1]
                    count += 1
            else:
                itemRate = rating[1]
        average = sumValue/count
        weight = pearson_correlation(user1, key)
        nominator += (itemRate - average) * weight
        denominator += math.fabs(weight)

    prediction = user1Average + (nominator/denominator)
    return prediction


runPrediction()



