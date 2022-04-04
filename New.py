import itertools
from collections import OrderedDict
from re import L


def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)

    return list


def listIsInList(l, L):
    ans = True
    for item in l:
        if item not in L:
            ans = False
    return ans


def itemSetIsInTransactions(l, processedTransactions):
    count = 0
    for line in processedTransactions:
        ans = True
        for item in l:
            if item not in line:
                ans = False
        if ans:
            count += 1
    #print(l, count)
    return count


def firstPartMatches(l, L):
    ans = True
    for i in range(0, len(l) - 1):
        # print(l[i])
        if l[i] not in L:
            ans = False
    return ans


def join(l1, l2):
    # print("last element of l2 - ", l2[-1])
    l1.append(l2[-1])
    # print(l1)
    return l1


def appriori(Lk, processedTransactions, k):
    L1 = OrderedDict(sorted(Lk.items()))
    L2 = L1
    #print(L1, L2)
    CandidateList = dict()
    for i in range(0, len(L1)):
        for j in range(i, len(L2)):
            l1 = getList(L1)[i]
            l2 = getList(L2)[j]
            l1 = list(l1)
            l2 = list(l2)
            #print("l1 = ", l1, "l2 = ", l2)
            if l1 == l2:
                continue
            if firstPartMatches(l1, l2):
                # print("l1 - ", (l1), "l2 - ",  l2, end = " , ")
                joined = join(l1, l2)
                # print("joined -", joined)
                for transaction in processedTransactions:
                    if listIsInList(joined, transaction):
                        joinedAsTuple = tuple(joined)
                        sup_count = itemSetIsInTransactions(joined, processedTransactions)
                        if joinedAsTuple in CandidateList.keys():
                            continue
                        else:
                            CandidateList[joinedAsTuple] = sup_count

    #print(CandidateList)
    FinalList = dict()
    for items in CandidateList:
        if CandidateList[items] >= min_sup:
            FinalList[items] = CandidateList[items]

    if (len(FinalList.keys()) == 1):
        return FinalList

    elif (len(FinalList.keys()) == 0):
        return Lk

    return appriori(FinalList, processedTransactions, min_sup)


file = open("database.txt", "r")
processedTransactions = []
frequencyofItems = dict()
for transaction in file:
    tempItems = transaction.split()
    items = []
    for item in tempItems:
        if item[-1] == ',':
            item = item[:-1]
        if item[0] == 'I':
            items.append(item)
            if (item, ) in frequencyofItems.keys():
                frequencyofItems[(item, ) ] += 1
            else:
                frequencyofItems[(item, ) ] = 1
    processedTransactions.append(items)
    # print(items)

#print("Processed Transactions", processedTransactions)
min_sup = 2
FinalList = dict()
for items in frequencyofItems:
    if frequencyofItems[items] >= min_sup:
        FinalList[items] = frequencyofItems[items]

#print(FinalList)
lastStepFrequencies = appriori(FinalList, processedTransactions, min_sup)
print(lastStepFrequencies)
