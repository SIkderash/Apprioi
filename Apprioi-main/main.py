import itertools


def get(possible_candidates, previousFrequenies, processedTransactions, nextLength, min_sup):
    frequencyOfSubsets = dict()
    for subset in itertools.combinations(possible_candidates, nextLength):
        # print(subset)
        # print(type(subset))
        for transaction in processedTransactions:
            subsetIsInThisTransaction = True
            for element in subset:
                if element not in transaction :
                    subsetIsInThisTransaction = False
            if subsetIsInThisTransaction:
                if subset in frequencyOfSubsets:
                    frequencyOfSubsets[subset] += 1
                else:
                    frequencyOfSubsets[subset] = 1
    # print(frequencyOfSubsets)
    possible_candidates.clear()
    possible_candidates = set()
    for subset in frequencyOfSubsets:
        if frequencyOfSubsets[subset] >= min_sup:
            #del(frequencyOfSubsets[subset])
            for element in subset:
                possible_candidates.add(element)
    possible_candidates = list(set(possible_candidates))
    possible_candidates = sorted(possible_candidates)
    # print(possible_candidates)
    if(len(possible_candidates)>2) :
        return get(possible_candidates, frequencyOfSubsets, processedTransactions, nextLength+1, min_sup)
    for singleSubset in frequencyOfSubsets:
        if frequencyOfSubsets[singleSubset] <min_sup:
            return previousFrequenies

    return frequencyOfSubsets

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

'''
for item in frequencyofItems:
    print(item, frequencyofItems[item])
'''
possible_candidates = []
# min_sup = int(input("Enter the minimum support value\n"))
min_sup = 2
for item in frequencyofItems:
    if frequencyofItems[item] >= min_sup:
        possible_candidates.append(item)
possible_candidates = sorted(possible_candidates)
# print(possible_candidates)


lastStepFrequencies = get(possible_candidates, frequencyofItems, processedTransactions, 2, min_sup)
ans = []
for subset in lastStepFrequencies:
    if lastStepFrequencies[subset]>=min_sup:
        ans.append(subset)

for tuple in ans:
    print(tuple)
