import itertools
from collections import OrderedDict

def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)
          
    return list

def appriori(List, processedTransactions, k):
    L1 = OrderedDict(sorted(List.items()))
    L2 = L1
    
    L_next = dict()
    for i in range (0, len(L1)):
        for j in range(i+1, len(L2)):
            firstPartOfL1 = getList(L1)[i]
            firstPartOfL2 = getList(L2)[j]
            print(firstPartOfL1, firstPartOfL2)

file = open("database.txt", "r")
processedTransactions = []
frequencyofItems = dict()
for transaction in file:
    tempItems = transaction.split()
    items = set()
    for item in tempItems:
        if item[-1] == ',':
            item = item[:-1]
        if item[0] == 'I':
            items.add(item)
            if item in frequencyofItems.keys():
                frequencyofItems[item] += 1
            else:
                frequencyofItems[item] = 1
    processedTransactions.append(items)
    # print(items)

min_sup = 2
for item in frequencyofItems:
    if frequencyofItems[item] < min_sup:
        del frequencyofItems[item]


lastStepFrequencies = appriori(frequencyofItems, processedTransactions, 1)
