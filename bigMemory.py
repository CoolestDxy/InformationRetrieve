from generateTerms import *
from boolOperator import *
from zoneOperator import *

# term按中文全拼排序
def sortCH(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


# 大内存下的n-gram索引查询
class bigMemoryModel:
    def __init__(self):
        self.termDic = None
        self.gramDic = None
        self.titleTerm = None
        self.carTerm = None

    # 输入通配符查询表达，返回term单词链表
    def searchTerm(self, query):
        searchGram = []
        if query[0] != '*':
            searchGram.append('$' + query[0])
        if query[-1] != '*':
            searchGram.append(query[-1] + '$')
        query = ''.join(query[1:-1].split('*'))
        for i in range(len(query)):
            searchGram.append(query[i])
        print(searchGram)
        search = []
        for s in searchGram:
            if s not in self.gramDic:
                print('no gram!:', s)
                return None
            search.append(self.gramDic[s])
        # for s in search:
        #     s.selfPrint()
        answer = MULTIGRAMAND(search)
        if answer == None:
            print('No term!')
            return None
        answer.selfPrint()
        return answer
    def replaceWildCard(self,query):
        querylist=query.split(' ')
        for q in querylist:
            if '*' in q:
                temp=self.searchTerm(q)
                words=[]
                while temp!=None:
                    words.append(temp.doc)
                    temp=temp.next
                replace='( '+' OR '.join(words)+' )'
                query=query.replace(q,replace)
        return query
    #基本查询，按词频排序
    def simpleSearch(self, query):
        #处理空格代替AND
        op='ANDNOTOR'
        query=query.split(' ')
        for i in range(len(query)):
            if i+1<len(query) and query[i] not in op and query[i+1] not in op:
                query.insert(i+1,'AND')
        query=' '.join(query)
        #处理通配符
        query = self.replaceWildCard(query)
        print(query)
        answer = search(query, self.termDic)
        if answer!=None:
            temp = answer
            sortList = []
            while temp != None:
                sortList.append(temp)
                temp = temp.next
            sortList.sort(key=sortedFreq, reverse=True)
            for i in range(len(sortList)):
                if i + 1 < len(sortList):
                    sortList[i].next = sortList[i + 1]
                else:
                    sortList[i].next = None
            sortList[0].selfPrint()
            return sortList[0]
        else:
            print('None')
            return None
    #域查询，按得分排序
    def zoneSearch(self, query):
        op = 'ANDNOTOR'
        query = query.split(' ')
        for i in range(len(query)):
            if i + 1 < len(query) and query[i] not in op and query[i + 1] not in op:
                query.insert(i + 1, 'AND')
        query = ' '.join(query)
        query = self.replaceWildCard(query)
        print(query)
        answer=ZoneSearch(query,self)
        if answer!=None:
            temp = answer
            sortList = []
            while temp != None:
                sortList.append(temp)
                temp = temp.next
            sortList.sort(key=sortedScore, reverse=True)
            for i in range(len(sortList)):
                if i + 1 < len(sortList):
                    sortList[i].next = sortList[i + 1]
                else:
                    sortList[i].next = None
            sortList[0].selfZonePrint()
            return sortList[0]
        return None


def sortedFreq(term):
    return term.freq
def sortedScore(term):
    return (term.title*0.3+term.term*0.1+term.car*0.6)

# 重写gram操作
def GRAMAND(node1, node2):
    tmp = None
    start = None
    i = 0
    while node1 != None and node2 != None:
        if sortCH(node1.doc) < sortCH(node2.doc):
            node1 = node1.next
        elif sortCH(node2.doc) < sortCH(node1.doc):
            node2 = node2.next
        else:
            if i == 0:
                p = PostNode(node1.doc, 0)
                tmp = p
                start = p
                i = 1
            else:
                p = PostNode(node1.doc, 0)
                tmp.next = p
                tmp = tmp.next
            node1 = node1.next
            node2 = node2.next
    # start.selfPrint()
    return start


def MULTIGRAMAND(terms):
    terms.sort(key=sortFreq)
    result = terms[0].postHead
    terms = rest(terms)
    while terms and result:
        result = GRAMAND(result, terms[0].postHead)
        terms = rest(terms)
    if result == None:
        print('None')
        return None
    # result.selfPrint()
    return result
def MultiQuery(model):
    while True:
        str = input("Enter your query(type'0' for searching term;'1' for simple search; '2' for zone search; 'exit' to quit ): ")
        if str=='exit':
            break
        elif str=='0':
            s = input('input wildcard query：')
            model.searchTerm(s)
        elif str=='1':
            s=input('input query：')
            model.simpleSearch(s)
        elif str=='2':
            s=input('input query：')
            model.zoneSearch(s)

if __name__ == '__main__':
    model = bigMemoryModel()
    model.termDic = getTerms()
    model.gramDic = getGrams()
    model.titleTerm = getTitleTerm()
    model.carTerm = getCarTerms()
    #ZoneSearch('奥迪 AND 改装 OR 疫情',model)
    MultiQuery(model)
    #model.replaceWildCard('代*')
    # for i in model.termDic:
    #     model.termDic[i].selfPrint()
    # for i in model.titleTerm:
    #     model.titleTerm[i].selfPrint()

    # for i in model.carTerm:
    #     print(i)
    #     model.carTerm[i].selfPrint()
    # test
    # target = '奥迪'
    # if target in model.carTerm:
    #     model.carTerm[target].selfPrint()
    # else:
    #     print('None carTerm')
    # if target in model.titleTerm:
    #     model.titleTerm[target].selfPrint()
    # else:
    #     print('None titleTerm')
    # if target in model.termDic:
    #     model.termDic[target].selfPrint()
    # else:
    #     print('None Term')
    # op1=getZoneNode(target,model)
    #
    # target1 = '改装'
    # if target1 in model.carTerm:
    #     model.carTerm[target1].selfPrint()
    # else:
    #     print('None carTerm')
    # if target1 in model.titleTerm:
    #     model.titleTerm[target1].selfPrint()
    # else:
    #     print('None titleTerm')
    # if target1 in model.termDic:
    #     model.termDic[target1].selfPrint()
    # else:
    #     print('None Term')
    # op2=getZoneNode(target1,model)
    # op2.selfPrint()
    # ZONEAND(op1,op2)
    # ZONEOR(op1, op2)
    # ZONEANDNOT(op1,op2)
    # #打印gram结构：
    # for i in model.gramDic:
    #     model.gramDic[i].selfPrintGram()
    # #查询测试：
    # model.searchTerm('代*')
    # model.zoneSearch('疫情 AND 奥迪 OR 改装')
