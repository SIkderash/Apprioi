import itertools
from collections import OrderedDict
from re import L

def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)
          
    return list

def listIsInList(l, L):
    if(all(x in L for x in l)):
        return True
    return False

def firstPartMatches(l, L):
    ans = True
    for i in range (0, len(l)-1):
        #print(l[i])
        if l[i] not in L:
            ans = False
    return ans

def join(l1, l2):
    L = l1.append(l2[-1])
    print(L)
    return L

def appriori(Lk, processedTransactions, k):
    L1 = OrderedDict(sorted(Lk.items()))
    L2 = L1
    #print(L1, L2)
    CandidateList = dict()
    for i in range (0, len(L1)):
        for j in range(0, len(L2)):
            l1 = getList(L1)[i]
            l2 = getList(L2)[j]
            l1 = l1.split(",")
            l2 = l2.split(",")
            #print("l1 - ", (l1), "l2 - ",  l2)
            if (l1 == l2):
                continue
            if firstPartMatches(l1, l2):
                print("l1 - ", (l1), "l2 - ",  l2, end = " , ")
                joined = join(l1, l2)
                print("joined -", joined)
                for transaction in processedTransactions:
                    if listIsInList(joined, transaction):
                        if joined in CandidateList.keys():
                            CandidateList[joined] += 1
                        else:
                            CandidateList[joined] = 1
    
    for items in CandidateList:
        if CandidateList[items]<min_sup:
            del CandidateList[items]

    if(len(CandidateList.keys())==1):
        return CandidateList
    
    elif(len(CandidateList.keys())==0):
        return Lk
    
    return appriori(CandidateList, processedTransactions, min_sup)
                        




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


lastStepFrequencies = appriori(frequencyofItems, processedTransactions, min_sup)
print(lastStepFrequencies)
