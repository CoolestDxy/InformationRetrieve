import os
import pickle
from dataStructure import *


#文章按序号排序
def sortTitle(title):
    return int(title.split('.')[0])
#从序列化文件获取term信息
def getTerms():
    with open('terms', 'rb') as file:
        term=pickle.load(file)
    return term
#获取文章列表
def getTitles():
    title=os.listdir('corpus/')
    title.sort(key=sortTitle)
    return title
#四种操作，传入为两个操作数的posting list
def ORNOT(node1, node2, MAX_ID):
    tmp = None
    start = None
    i = 0
    id = 0
    while id < MAX_ID:
        if node1 != None and node1.doc == id:
            if i == 0:
                p = PostNode(node1.doc)
                tmp = p
                start = p
                i = 1
            else:
                p = PostNode(node1.doc)
                tmp.next = p
                tmp = tmp.next
            node1 = node1.next
            if node2.doc == id:
                node2 = node2.next
        elif node2.doc == id:
            node2 = node2.next
        else:
            if i == 0:
                p = PostNode(id)
                tmp = p
                start = p
                i = 1
            else:
                p = PostNode(id)
                tmp.next = p
                tmp = tmp.next
        id = id + 1
    #start.selfPrint()
    return start

def OR(node1, node2):
    tmp=None
    start=None
    i = 0
    while node1 != None and node2 != None:
        if node1.doc < node2.doc:
            if i == 0:
                p = PostNode(node1.doc,node1.freq)
                tmp= p
                start = p
                i = 1
            else:
                p = PostNode(node1.doc,node1.freq)
                tmp.next = p
                tmp = tmp.next
            node1 = node1.next
        elif node2.doc < node1.doc:
            if i == 0:
                p = PostNode(node2.doc,node2.freq)
                tmp = p
                start = p
                i = 1
            else:
                p = PostNode(node2.doc,node2.freq)
                tmp.next = p
                tmp = tmp.next
            node2 = node2.next
        else:
            if i == 0:
                p = PostNode(node1.doc,node1.freq+node2.freq)
                tmp = p
                start = p
                i = 1
            else:
                p = PostNode(node1.doc,node1.freq+node2.freq)
                tmp.next = p
                tmp = tmp.next
            node1 = node1.next
            node2 = node2.next
    while node1 != None:
        if i == 0:
            p = PostNode(node1.doc,node1.freq)
            tmp = p
            start = p
            i = 1
        else:
            p = PostNode(node1.doc,node1.freq)
            tmp.next = p
            tmp = tmp.next
        node1 = node1.next
    while node2 != None:
        if i == 0:
            p = PostNode(node2.doc,node2.freq)
            tmp = p
            start = p
            i = 1
        else:
            p = PostNode(node2.doc,node2.freq)
            tmp.next = p
            tmp = tmp.next
        node2 = node2.next
    #start.selfPrint()
    return start


def ANDNOT(node1, node2):
    tmp=None
    start=None
    i = 0
    while node1 != None and node2 != None:
        if node1.doc < node2.doc:
            if i == 0:
                p = PostNode(node1.doc,node1.freq)
                tmp = p
                start = p
                i = 1
            else:
                p = PostNode(node1.doc,node1.freq)
                tmp.next = p
                tmp = tmp.next
            node1 = node1.next
        elif node1.doc == node2.doc:
            node1 = node1.next
            node2 = node2.next
        else:
            node2 = node2.next
    while node1 != None:
        p = PostNode(node1.doc,node1.freq)
        tmp.next = p
        tmp = tmp.next
        node1 = node1.next
    #start.selfPrint()
    return start

def AND(node1, node2):
    tmp = None
    start = None
    i = 0
    while node1 != None and node2 != None:
        if node1.doc < node2.doc:
            node1 = node1.next
        elif node2.doc < node1.doc:
            node2 = node2.next
        else:
            if i == 0:
                p = PostNode(node1.doc, node1.freq+node2.freq)
                tmp = p
                start = p
                i = 1
            else:
                p = PostNode(node1.doc, node1.freq+node2.freq)
                tmp.next = p
                tmp = tmp.next
            node1 = node1.next
            node2 = node2.next
    #start.selfPrint()
    return start

def sortFreq(term):
    return term.freq
#取剩余term项
def rest(termList):
    if len(termList)<=1:
        return None
    return termList[1:]

#多个AND查询优化
def MULTIAND(terms):
    terms.sort(key=sortFreq)
    result=terms[0].postHead
    terms=rest(terms)
    while terms and result:
        result=AND(result,terms[0].postHead)
        terms=rest(terms)
    if result==None:
        print('None')
        return None
    result.selfPrint()
    return result

#运算符优先级
def compare(op1, op2):
    return op1 in ["AND", "ANDNOT"] and op2 in ["OR", "ORNOT"]

#运算
def getvalue(num1, num2, operator):
    if operator == "AND":
        return AND(num1,num2)
    elif operator == "ANDNOT":
        return ANDNOT(num1,num2)
    elif operator == "OR":
        return OR(num1,num2)
    elif operator == "ORNOT":
        return ORNOT(num1,num2,75)
    else:
        print('illegal Operation')
        return None

#出栈入栈
def process(data, opt):
    operator = opt.pop()
    num2 = data.pop()
    num1 = data.pop()
    #print(num1,num2,operator)
    data.append(getvalue(num1, num2, operator))

#查询答案
def search(query,termDic):
    s=query.split(' ')
    if len(s)==1:
        if s[0] not in termDic:
            print('NO term:',s[0])
            return None
        else:
            termDic[s[0]].postHead.selfPrint()
            return termDic[s[0]].postHead
    i=0
    flag=True
    multi=[]
    while i<len(s):
        if i%2==1 and s[i]!='AND':
            flag=False
        elif i%2==0:
            multi.append(s[i])
        i+=1
    if flag:
        temp=[]
        for t in multi:
            if t not in termDic:
                print('term error: ',t)
                return None
            temp.append(termDic[t])
        return MULTIAND(temp)
    operator='ORANDNOT()'
    data = []  # 数据栈
    opt = []  # 操作符栈
    i = 0  # 表达式遍历索引
    while i < len(s):
        if s[i] not in operator:  # 入栈data
            if s[i] not in termDic:
                print('illegal term!:',s[i])
                return None
            data.append(termDic[s[i]].postHead)
        elif s[i] == ")":  # 右括号，opt出栈同时data出栈并计算，计算结果入栈data，直到opt出栈一个左括号
            while opt[-1] != "(":
                process(data, opt)
            opt.pop()  # 出栈"("
        elif not opt or opt[-1] == "(":  # 操作符栈为空，或者操作符栈顶为左括号，操作符直接入栈opt
            opt.append(s[i])
        elif s[i] == "(" or compare(s[i], opt[-1]):  # 当前操作符为左括号或者比栈顶操作符优先级高，操作符直接入栈opt
            opt.append(s[i])
        else:  # 优先级不比栈顶操作符高时，opt出栈同时data出栈并计算，计算结果如栈data
            while opt and not compare(s[i], opt[-1]):
                if opt[-1] == "(":  # 若遇到左括号，停止计算
                    break
                process(data, opt)
            opt.append(s[i])
        i += 1  # 遍历索引后移
    while opt:
        process(data, opt)
    result=data.pop()
    if result!=None:
        result.selfPrint()
        return result
    return None

def query(termDic):
    while True:
        str = input("Enter your query(type 'exit' to quit ): ")
        if str=='exit':
            break
        else:
            search(str,termDic)

if __name__ == '__main__':
    titleList=getTitles()
    termDic=getTerms()
        #t.selfPrint()
    # print('\noperation test:')
    # termList[termDic['做工']].selfPrint()
    # termList[termDic['座椅']].selfPrint()
    # #search('最新 AND 科技 ANDNOT 左右 OR 座舱 AND 做工')
    #最新 AND ( 科技 OR 座椅 ) AND 做工
    query(termDic)
