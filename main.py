from enum import unique
import itertools
from collections import OrderedDict
from re import L
import tkinter as tk
from tkinter import *
class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='Input 1')
        self.lbl2=Label(win, text='Input 2')
        self.lbl3=Label(win, text='Result')
        self.t1=Entry(bd=3)
        self.t2=Entry()
        self.t3=Entry()
        self.btn1 = Button(win, text='Add')
        self.btn2=Button(win, text='Calculate')
        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=100)
        self.b1=Button(win, text='Add', command=self.add)
        self.b2=Button(win, text='Calculate')
        self.b2.bind('<Button-1>', self.calculate)
        self.b1.place(x=100, y=150)
        self.b2.place(x=200, y=150)
        self.lbl3.place(x=100, y=200)
        self.t3.place(x=200, y=200)
    def add(self):
        file = open("database.txt", "a")
        self.t3.delete(0, 'end')
        file.writelines("\n" + self.t1.get())
        self.t3.insert(END, "Added!!")
    def calculate(self, event):
        file = open("database.txt", "a")
        self.t3.delete(0, 'end')
        num1=int(self.t1.get())
        num2=int(self.t2.get())
        result=num1-num2
        self.t3.insert(END, str(result))

window=Tk()
mywin=MyWindow(window)
window.title('Confidence Calculator')
window.geometry("400x300+10+10")
window.mainloop()


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


def appriori(Lk, processedTransactions, k, sup_counter):
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
        sup_counter[items] = CandidateList[items]
        if CandidateList[items] >= min_sup:
            FinalList[items] = CandidateList[items]

    if (len(FinalList.keys()) == 1):
        return FinalList, sup_counter

    elif (len(FinalList.keys()) == 0):
        return Lk, sup_counter

    return appriori(FinalList, processedTransactions, min_sup, sup_counter)


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
sup_counter = frequencyofItems
lastStepFrequencies, sup_counter = appriori(FinalList, processedTransactions, min_sup, sup_counter)
#print(lastStepFrequencies)
#print(sup_counter)
user_input_A = input("Enter itemset A\n")
user_input_B = input("Enter itemset B\n")
itemList_A = sorted(user_input_A.split())
itemList_B = sorted(user_input_B.split())
formatted_A = tuple(itemList_A)

union_set = itemList_A
for items in itemList_B:
    union_set.append(items)

union_set = sorted(list(set(union_set)))
#print(tuple(union_set))

print(sup_counter[tuple(union_set)])
print(sup_counter[formatted_A])
print("The confidence P(A=>B) = ", sup_counter[tuple(union_set)]/sup_counter[formatted_A])
