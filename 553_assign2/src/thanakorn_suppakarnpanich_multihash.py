#class

_author_ = 'thanakorn suppakarnpanich'

import sys
import itertools


def runMultihash():
    fileName = sys.argv[1]
    support = int(sys.argv[2])
    bucket = int(sys.argv[3])
    inFile = open(fileName, 'r')
    frequentItemset = []
    itemIdDictionary = {}
    itemCountDictionary = {}
    itemId = 0;
    k = 1
    kMax = getMaxTuplesNumber(fileName)
    while k <= kMax:
        tuples = createItemTuples(k)

        itemCountDictionary = makeItemCountDictionary(tuples) #get item counts
        frequentItemDictionary = makeFrequentItemDictionary(itemCountDictionary, support)

        hashTable1 = createHashTable(k+1, fileName, bucket, 1) #hash item tuples to hashtable 1
        hashTable2 = createHashTable(k+1, fileName, bucket, 7) #hash item tuples to hashtable 2

        bitmap1 = CreateBitMap(hashTable1, support, bucket)
        bitmap2 = CreateBitMap(hashTable2, support, bucket)


        #find frequent itemsets
        k = k + 1


def createHashTable(k, fileName, bucket, randomConstant):
    hashTable = {}
    tuples = createItemTuples(k)
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


def CreateBitMap(hashTable, support, bucket):
    bitmap = [0] * bucket
    for key, value in hashTable.items():
        if(value >= support):
            bitmap[key] = 1
        else:
            bitmap[key] = 0
    return bitmap


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
        itemset = [list(x) for x in itertools.combinations(listArray, k)]
        for each in itemset:
            each.sort()
            result.append(each)
    result.sort()
    return result


runMultihash()




