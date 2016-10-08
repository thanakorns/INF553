_author_ = 'thanakorn suppakarnpanich'

import sys
import itertools
import random
import copy


def runToivonen():
    fileName = sys.argv[1]
    inputSupport = int(sys.argv[2])
    inFile = open(fileName, 'r')
    baskets = createBaskets(inFile)
    probability = 0.5
    iteration = 0
    while True:
        #first pass
        sample = randomsampling(baskets, probability)
        fraction = probability
        support = inputSupport*probability*0.8
        allItemsets = createAllItemSets(sample)
        itemCountDictionary = makeItemCountDictionary(allItemsets)
        itemToIdDictionary = makeItemToIdDictionary(allItemsets)
        idToItemDictionary = makeIdToItemDictionary(itemToIdDictionary)
        splittedItemSets = splitFrequentAndNotFrequentItemSets(itemCountDictionary, support, idToItemDictionary)
        sampleFrequentItemSets = splittedItemSets[0]
        sampleNotFrequentItemSets = splittedItemSets[1]
        negativeBorder = makeNegativeBorder(sampleNotFrequentItemSets, sampleFrequentItemSets)

        #second pass
        frequentItemset = processWholeFile(sampleFrequentItemSets, negativeBorder, baskets, inputSupport)
        if frequentItemset:
            iteration = iteration + 1
            print iteration
            print fraction
            frequentItemset = formatFrequentItemSet(frequentItemset)
            for eachItemset in frequentItemset:
                print eachItemset
                print ("\n")
            break
        iteration = iteration + 1


def formatFrequentItemSet(frequentItemset):
    frequentItemset.sort()
    maxLength = 0
    for each in frequentItemset:
        if len(each) > maxLength:
            maxLength = len(each)
    newArray = [[] for i in range(maxLength)]
    for each in frequentItemset:
        newArray[len(each)-1].append(each)
    return newArray


def processWholeFile(sampleFrequentItemSets, negativeBorder, baskets, inputSupport):
    trulyFrequent = []
    negativeBorderContainFrequentItemset = 0
    for itemSet in negativeBorder:
        count = 0
        for basket in baskets:
            shouldCount = 1
            for item in itemSet:
                if not basket.__contains__(item):
                    shouldCount = 0
                    break
            if shouldCount == 1:
                count = count + 1
        if count >= inputSupport:
            negativeBorderContainFrequentItemset = 1
            break

    if negativeBorderContainFrequentItemset == 0:
        for itemSet in sampleFrequentItemSets:
            count = 0
            for basket in baskets:
                shouldCount = 1
                for item in itemSet:
                    if not basket.__contains__(item):
                        shouldCount = 0
                        break
                if shouldCount == 1:
                    count = count + 1
            if count >= inputSupport:
                trulyFrequent.append(itemSet)
    return trulyFrequent


def randomsampling(baskets, probability):
    size = len(baskets)
    result = random.sample(baskets, int(probability*size))
    return result


def createBaskets(inFile):
    baskets = []
    for line in inFile:
        basketArray = []
        basket = line.split(",")
        for each in basket:
            each = each.rstrip("\n")
            basketArray.append(each)
        baskets.append(basketArray)
    return baskets


def createAllItemSets(sample):
    k = 1
    allItemsets = []
    while True:
        tuples = createItemTuples(k, sample)
        allItemsets = allItemsets + tuples
        k = k + 1
        if not tuples:
            break
    return allItemsets


def splitFrequentAndNotFrequentItemSets(itemCountDictionary, support, idToItemDictionary):

    frequentItemSets = []
    notFrequentItemSets = []
    for key, value in itemCountDictionary.items():
        if value >= support:
            frequentItemSet = idToItemDictionary[key]
            frequentItemSet = list(itertools.chain.from_iterable(frequentItemSet))
            frequentItemSets.append(frequentItemSet)
        else:
            notFrequentItemSet = idToItemDictionary[key]
            notFrequentItemSet = list(itertools.chain.from_iterable(notFrequentItemSet))
            notFrequentItemSets.append(list(notFrequentItemSet))
    result = []
    result.append(frequentItemSets)
    result.append(notFrequentItemSets)
    return result


def makeNegativeBorder(sampleNotFrequentItemSets, sampleFrequentItemSets):
    negativeBorder = []
    for itemSet in sampleNotFrequentItemSets:
        shouldCount = 1
        for i in range(0, len(itemSet)):
            tempSet = copy.copy(itemSet)
            del tempSet[i]
            if not sampleFrequentItemSets.__contains__(tempSet):
                shouldCount = 0
                break
        if shouldCount == 1:
            negativeBorder.append(itemSet)
    return negativeBorder


def createItemsets(listTemp, k):
    listArray = [list(x) for x in itertools.combinations(listTemp, k)]
    return listArray


def createItemTuples(k, baskets):
    result = []
    for basket in baskets:
        basket.sort()
        listArray = []
        for each in basket:
            each = each.rstrip("\n")
            listArray.append(each)
        itemset = createItemsets(listArray, k)
        for each in itemset:
            each.sort()
            result.append(each)
    return result


def makeItemCountDictionary(tuples):
    itemIdDictionary = {}
    itemCountDictionary = {}
    itemId = 0;
    for each in tuples:
        each = makeStringFromTuple(each)
        if not itemIdDictionary.__contains__(each):
            itemIdDictionary[each] = itemId
            itemId = itemId + 1
        if itemCountDictionary.__contains__(itemIdDictionary[each]):
            count = itemCountDictionary[itemIdDictionary[each]]
            count = count + 1
            itemCountDictionary[itemIdDictionary[each]] = count
        else:
            itemCountDictionary[itemIdDictionary[each]] = 1
    return itemCountDictionary


def makeItemToIdDictionary(tuples):
    itemIdDictionary = {}
    itemId = 0;
    for each in tuples:
        each = makeStringFromTuple(each)
        if not itemIdDictionary.__contains__(each):
            itemIdDictionary[each] = itemId
            itemId = itemId + 1
    return itemIdDictionary


def makeIdToItemDictionary(itemToIdDictionary):
    idToItemDictionary = {}
    for key, value in itemToIdDictionary.items():
        tempList = list()
        for i in range(0, len(key)):
            tempList.append(key[i])
        itemTuple = tuple(tempList)
        idToItemDictionary[value] = itemTuple
    return idToItemDictionary


def makeStringFromTuple(tuple):
    key = ''.join(tuple)
    return key


runToivonen()