class PostNode:
    def __init__(self, doc, freq=0,car=0, title=0, term=0):
        self.doc = doc
        self.freq = freq
        self.next = None
        self.car = car
        self.title = title
        self.term = term

    def selfPrint(self):
        print('PostNode: {' + str(self.doc) + ',' + str(round(self.freq, 2)) + '}', end='')
        temp = self.next
        while temp != None:
            print('->{' + str(temp.doc) + ',' + str(round(temp.freq, 2)) + '}', end='')
            temp = temp.next
        print()
    def selfZonePrint(self):
        print('PostNode: {' + str(self.doc) + ',' + str(self.title*0.3+self.term*0.1+self.car*0.6) + '}', end='')
        temp = self.next
        while temp != None:
            print('->{' + str(temp.doc) + ',' + str(temp.title*0.3+temp.term*0.1+temp.car*0.6) + '}', end='')
            temp = temp.next
        print()

class TermNode:
    def __init__(self, term, freq, node):
        self.term = term
        self.freq = freq
        self.docNum = 1
        self.postHead = node

    def addPostNode(self, node):
        if self.postHead == None:
            self.postHead = node
        else:
            temp = self.postHead
            last = None
            while temp != None and temp.doc < node.doc:
                last = temp
                temp = temp.next
            if last != None:
                last.next = node
            node.next = temp

    def addNode(self, node):
        flag = 0
        temp = self.postHead.next
        last = self.postHead
        if last.doc == node.doc:
            flag = 1
        while temp != None:
            if temp.doc == node.doc:
                flag = 1
            last = temp
            temp = temp.next
        if flag == 0:
            last.next = node
            self.freq += 1

    def selfPrint(self):
        print('term: ' + self.term + ' freq: ' + str(self.freq) + ' docNum: ' + str(self.docNum))
        temp = self.postHead
        while temp != None:
            print('->{' + str(temp.doc) + ',' + str(temp.freq) + '}', end='')
            temp = temp.next
        print()

    def selfPrintGram(self):
        print('gram: ' + self.term + ' freq: ' + str(self.freq))
        temp = self.postHead
        while temp != None:
            print('->' + str(temp.doc), end='')
            temp = temp.next
        print()
# class GramPostNode:
#     def __init__(self,term):
#         self.next=None
#         self.term=term
# class GramNode:
#     def __init__(self,gram,term):
#         self.gram=gram
#         self.head=term
#     def addNode(self,node):
#         flag=0
#         temp=self.head.next
#         last=self.head
#         if last.term == node.term:
#             flag = 1
#         while temp!=None:
#             if temp.term==node.term:
#                 flag=1
#             last=temp
#             temp=temp.next
#         if flag==0:
#             last.next=node
#     def selfPrint(self):
#         print('term: '+self.gram)
#         temp=self.head
#         while temp!=None:
#             print('->'+str(temp.term), end='')
#             temp=temp.next
#         print()
