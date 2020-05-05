import jieba
import pypinyin
import os
import pickle
from collections import OrderedDict
from dataStructure import *
digital='1234567890.'
r1= "[\s+\.\!\/_,$%^*(+\"\']+|[　『』+®——！，。？=>、~@#￥%……&*（）)]【】●éá:×+---...... ；：！？｡＂＃＄％＆＇ （）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～､、〃》「」–—‘’‛“”„‟…‧﹏. °·。《("
#去除数字
def totalDigital(s):
    flag=0
    for i in range(len(s)):
        if s[i] not in digital:
            return False
    return True
def containDigital(s):
    flag=0
    for i in range(len(s)):
        if s[i] in digital:
            return True
    return False
#term按中文全拼排序
def sortKey(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s
#文章按序号排序
def sortTitle(title):
    return int(title.split('.')[0])
#生成term信息
def generateTerms(filelist):
    termDic = {}
    filelist.sort(key=sortTitle)
    print(filelist)
    for index in range(len(filelist)):
        with open('corpus/'+filelist[index], 'r', encoding='utf-8')as f:
            content = f.read()
        parse = jieba.lcut(content)
        term = []
        for p in parse:
            if p in r1 or len(p.replace(' ',''))==0 or containDigital(p):
                continue
            term.append(p)
        temp = {}
        for word in term:
            if word in temp:
                temp[word] += 1
            else:
                temp[word] = 1
        for word in temp:
            if word not in termDic:
                termDic[word]=TermNode(word, temp[word], PostNode(index,temp[word]))
            else:
                termDic[word].docNum += 1
                termDic[word].freq += temp[word]
                termDic[word].addPostNode(PostNode(index,temp[word]))
    sortedKeys=sorted(termDic.keys(),key=sortKey)
    sortedTerm=OrderedDict()
    for key in sortedKeys:
        sortedTerm[key]=termDic[key]
    for t in sortedTerm:
        sortedTerm[t].selfPrint()
    with open('terms','wb')as file:
        pickle.dump(sortedTerm,file)

#N-gram索引
def generateNgram(termDic):
    gramDic={}
    for term in termDic.keys():
        for i in range(0,len(term)):
            temp=term[i]
            if i==0:
                prex='$'+temp
                if prex not in gramDic:
                    gramDic[prex] = TermNode(prex,1, PostNode(term))
                else:
                    gramDic[prex].addNode(PostNode(term))
            if i==len(term)-1:
                suffix = temp+'$'
                if suffix not in gramDic:
                    gramDic[suffix] = TermNode(suffix,1, PostNode(term))
                else:
                    gramDic[suffix].addNode(PostNode(term))
            if temp not in gramDic:
                gramDic[temp]=TermNode(temp,1,PostNode(term))
            else:
                gramDic[temp].addNode(PostNode(term))
    sortedGram=OrderedDict()
    sortedKeys = sorted(gramDic.keys(), key=sortKey)
    for key in sortedKeys:
        sortedGram[key]=gramDic[key]
    for g in sortedGram:
        sortedGram[g].selfPrintGram()
    with open('grams','wb')as file:
        pickle.dump(sortedGram,file)
#汽车文章标题索引
def generateTitleTerm():
    termDic = {}
    title=getTitle()
    for index in range(len(title)):
        parse = jieba.lcut(''.join(''.join(title[index].split('.')[1:-1]).split('_')[1:]))
        term = []
        for p in parse:
            if p in r1 or len(p.replace(' ',''))==0 or totalDigital(p):
                continue
            term.append(p)
        temp = {}
        for word in term:
            if word in temp:
                temp[word] += 1
            else:
                temp[word] = 1
        for word in temp:
            if word not in termDic:
                termDic[word]=TermNode(word, temp[word], PostNode(index,temp[word]))
            else:
                termDic[word].docNum += 1
                termDic[word].freq += temp[word]
                termDic[word].addPostNode(PostNode(index,temp[word]))
    sortedKeys=sorted(termDic.keys(),key=sortKey)
    sortedTerm=OrderedDict()
    for key in sortedKeys:
        sortedTerm[key]=termDic[key]
    for t in sortedTerm:
        sortedTerm[t].selfPrint()
    with open('titleTerms','wb')as file:
        pickle.dump(sortedTerm,file)
#汽车名称索引
def generateCarTerm():
    termDic = {}
    title=getTitle()
    for index in range(len(title)):
        parse = jieba.lcut(''.join(''.join(title[index].split('.')[1:-1]).split('_')[0]))
        term = []
        for p in parse:
            if p in r1 or len(p.replace(' ',''))==0 or totalDigital(p):
                continue
            term.append(p)
        temp = {}
        for word in term:
            if word in temp:
                temp[word] += 1
            else:
                temp[word] = 1
        for word in temp:
            if word not in termDic:
                termDic[word]=TermNode(word, temp[word], PostNode(index,temp[word]))
            else:
                termDic[word].docNum += 1
                termDic[word].freq += temp[word]
                termDic[word].addPostNode(PostNode(index,temp[word]))
    sortedKeys=sorted(termDic.keys(),key=sortKey)
    sortedTerm=OrderedDict()
    for key in sortedKeys:
        sortedTerm[key]=termDic[key]
    for t in sortedTerm:
        sortedTerm[t].selfPrint()
    with open('CarTerms','wb')as file:
        pickle.dump(sortedTerm,file)
#获取gram index数据
def getGrams():
    with open('grams', 'rb') as file:
        gram=pickle.load(file)
    return gram
#获取文章名
def getTitle():
    path = "corpus/"
    filename_list = os.listdir(path)
    filename_list.sort(key=sortTitle)
    return filename_list
#从序列化文件获取term信息
def getTerms():
    with open('terms', 'rb') as file:
        term=pickle.load(file)
    return term
def getTitleTerm():
    with open('titleTerms', 'rb') as file:
        term=pickle.load(file)
    return term
def getCarTerms():
    with open('CarTerms', 'rb') as file:
        term=pickle.load(file)
    return term
if __name__ == '__main__':
    # path = "corpus/"
    # filename_list = os.listdir(path)
    # generateTerms(filename_list)
    # tlist=getTerms()
    # generateNgram(tlist)
    # grams=getGrams()
    # for g in grams:
    #     grams[g].selfPrintGram()
    # generateTitleTerm()
    car=getCarTerms()
    for c in car:
        car[c].selfPrint()