_author_ = 'thanakorn suppakarnpanich'

import sys
import itertools


def runMultihash():
    fileName = sys.argv[1]
    support = int(sys.argv[2])
    bucket = int(sys.argv[3])
    inFile = open(fileName, 'r')
    frequentItemset = []
    idToItemDictionary = {}
    itemCountDictionary = {}
    candidateItemArray = {}
    printedHashTable1 = {}
    printedHashtable2 = {}
    itemId = 0;
    k = 1
    kMax = getMaxTuplesNumber(fileName)
    for k in range(1, kMax):
        tuples = createItemTuples(k)
        if k == 1:
            candidateItemArray = sort_and_deduplicate(tuples)

        itemCountDictionary = makeItemCountDictionary(tuples) #get item counts
        itemToIdDictionary = makeItemToIdDictionary(tuples)
        idToItemDictionary = makeIdToItemDictionary(itemToIdDictionary)

        nextTuples = createItemTuples(k+1)
        hashTable1 = createHashTable(nextTuples, bucket, 1) #hash item tuples to hashtable 1
        hashTable2 = createHashTable(nextTuples, bucket, 7) #hash item tuples to hashtable 2

        # print sorted(candidateItemArray)
        #2nd pass
        frequentItemset = makeFrequentItemset(candidateItemArray, itemCountDictionary, idToItemDictionary, itemToIdDictionary, support, k)
        bitmap1 = createBitMap(hashTable1, support, bucket)
        bitmap2 = createBitMap(hashTable2, support, bucket)
        itemToIdDictionaryForNextTuples = makeItemToIdDictionary(nextTuples)
        candidateItemArray = makeCandidateItemArray(nextTuples, itemToIdDictionaryForNextTuples, frequentItemset, support, bitmap1, bitmap2, 1, 7, bucket, k)

        if not frequentItemset:
            break;
        if k != 1:
            print ("\n")
            print printedHashTable1
            print printedHashtable2
        print (sorted(frequentItemset))
        printedHashTable1 = hashTable1
        printedHashtable2 = hashTable2


def makeFrequentItemset(candidateItemArray, itemCountDictionary, idToItemDictionary, itemToIdDictionary, support, k):
    frequentItemSet = []
    frequentList = []
    for tuple in candidateItemArray:
        key = makeStringFromTuple(tuple)
        if(itemCountDictionary[itemToIdDictionary[key]] >= support):
            frequentItemSet.append(idToItemDictionary[itemToIdDictionary[key]])
    if k == 1:
        frequentList = list(itertools.chain.from_iterable(frequentItemSet))
    else:
        for eachTuple in frequentItemSet:
            frequentList.append(list(itertools.chain.from_iterable(eachTuple)))
    return frequentList


def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def sort_and_deduplicate(l):
    return list(uniq(sorted(l, reverse=True)))


def makeCandidateItemArray(nextTuples, itemToIdDictionary, frequentItemset, support, bitmap1, bitmap2, randomConstant1, randomConstant2, bucket, k):
    setTuples = sort_and_deduplicate(nextTuples)
    candidateItemArray = []
    for each in setTuples:
        components = createItemsets(each, k)
        if k == 1:
            newListArray = []
            for eachCombinationList in components:
                for eachLetter in eachCombinationList:
                    newListArray.append(eachLetter)
            components = newListArray

        candidate = 1
        for eachComponent in components:
            if not eachComponent in frequentItemset:
                # print "component error: " + eachComponent + " " + str(frequentItemset)
                candidate = 0
                break
        if itemToIdDictionary.__contains__(makeStringFromTuple(each)):
            key = itemToIdDictionary[makeStringFromTuple(each)]
            if not bitmap1[(randomConstant1 + key) % bucket] == 1:
                # print "bitmap1 error: " +  str(bitmap1[(randomConstant1+key) % bucket]) + " " + str(support)
                candidate = 0
            if not bitmap2[(randomConstant2 + key) % bucket] == 1:
                # print "bitmap2 error: " +  str(bitmap1[(randomConstant2+key) % bucket]) + " " + str(support)
                candidate = 0
        if candidate == 1:
            candidateItemArray.append(list(each))
    # if k == 2:
    #     print sorted(candidateItemArray)
    return candidateItemArray


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


def createHashTable(tuples, bucket, randomConstant):
    hashTable = {}
    itemCountDictionary = makeItemCountDictionary(tuples)
    for i in range(0, bucket):
        hashTable[i] = 0
    for key, value in itemCountDictionary.items():
        hashKey = (randomConstant+key)%bucket
        count = hashTable[hashKey]
        count = count + 1
        hashTable[hashKey] = count
    return hashTable


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


def makeStringFromTuple(tuple):
    key = ''.join(tuple)
    return key


def getMaxTuplesNumber(fileName):
    inFile = open(fileName, 'r')
    kMax = 0
    for line in inFile:
        basket = line.split(",")
        if(len(basket) > kMax):
            kMax = len(basket)
    return kMax


def createBitMap(hashTable, support, bucket):
    bitmap = [0] * bucket
    for key, value in hashTable.items():
        if(value >= support):
            bitmap[key] = 1
        else:
            bitmap[key] = 0
    return bitmap


def createItemsets(listTemp, k):
    listArray=[list(x) for x in itertools.combinations(listTemp, k)]
    return listArray


def createItemTuples(k):
    inFile = open(sys.argv[1], 'r')
    result = []
    for line in inFile:
        listArray = []
        itemArray = line.split(",")
        itemArray.sort()
        for each in itemArray:
            each = each.rstrip("\n")
            listArray.append(each)
        itemset = createItemsets(listArray, k)
        for each in itemset:
            each.sort()
            result.append(each)
    result.sort()
    return result


runMultihash()




