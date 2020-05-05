from dataStructure import *
def getZoneNode(s,model):
    car = None
    title = None
    term = None
    if s in model.carTerm:
        car = model.carTerm[s].postHead
    if s in model.titleTerm:
        title = model.titleTerm[s].postHead
    if s in model.termDic:
        term = model.termDic[s].postHead
    ans = None
    tmp = None
    while car is not None and title is not None:
        if car.doc < title.doc:
            if ans is None:
                ans = PostNode(car.doc, 0, 1, 0, 0)
                tmp = ans
            else:
                ans.next = PostNode(car.doc, 0, 1, 0, 0)
                ans = ans.next
            car = car.next
        elif car.doc > title.doc:
            if ans is None:
                ans = PostNode(title.doc, 0, 0, 1, 0)
                tmp = ans
            else:
                ans.next = PostNode(title.doc, 0, 0, 1, 0)
                ans = ans.next
            title = title.next
        else:
            if ans is None:
                ans = PostNode(car.doc, 0, 1, 1, 0)
                tmp = ans
            else:
                ans.next = PostNode(car.doc, 0, 1, 1, 0)
                ans = ans.next
            car = car.next
            title = title.next
    while car is not None:
        if ans is None:
            ans = PostNode(car.doc, 0, 1, 0, 0)
            tmp = ans
        else:
            ans.next = PostNode(car.doc, 0, 1, 0, 0)
            ans = ans.next
        car = car.next
    while title is not None:
        if ans is None:
            ans = PostNode(title.doc, 0, 0, 1, 0)
            tmp = ans
        else:
            ans.next = PostNode(title.doc, 0, 0, 1, 0)
            ans = ans.next
        title = title.next
    ans = tmp
    # ans.selfZonePrint()

    ans1 = None
    rt = ans1
    while ans is not None and term is not None:
        if ans.doc < term.doc:
            if ans1 is None:
                ans1 = PostNode(ans.doc, 0, ans.car, ans.title, 0)
                rt = ans1
            else:
                ans1.next = PostNode(ans.doc, 0, ans.car, ans.title, 0)
                ans1 = ans1.next
            ans = ans.next
        elif ans.doc > term.doc:
            if ans1 is None:
                ans1 = PostNode(term.doc, 0, 0, 0, 1)
                rt = ans1
            else:
                ans1.next = PostNode(term.doc, 0, 0, 0, 1)
                ans1 = ans1.next
            term = term.next
        else:
            if ans1 is None:
                ans1 = PostNode(ans.doc, 0, ans.car, ans.title, 1)
                rt = ans1
            else:
                ans1.next = PostNode(ans.doc, 0, ans.car, ans.title, 1)
                ans1 = ans1.next
            ans = ans.next
            term = term.next
    while ans is not None:
        if ans1 is None:
            ans1 = PostNode(ans.doc, 0, ans.car, ans.title, 0)
            rt = ans1
        else:
            ans1.next = PostNode(ans.doc, 0, ans.car, ans.title, 0)
            ans1 = ans1.next
        ans = ans.next
    while term is not None:
        if ans1 is None:
            ans1 = PostNode(term.doc, 0, 0, 0, 1)
            rt = ans1
        else:
            ans1.next = PostNode(term.doc, 0, 0, 0, 1)
            ans1 = ans1.next
        term = term.next
    if rt==None:
        print('No term!:',s)
        return None
    else:
        #rt.selfZonePrint()
        return rt

def ZONEANDNOT(node1, node2):
    tmp=None
    start=None
    i = 0
    while node1 != None and node2 != None:
        if node1.doc < node2.doc:
            if start is None:
                tmp = PostNode(node1.doc, 0,node1.car,node1.title,node1.term)
                start = tmp
            else:
                tmp.next = PostNode(node1.doc, 0,node1.car,node1.title,node1.term)
                tmp = tmp.next
            node1 = node1.next
        elif node1.doc == node2.doc:
            node1 = node1.next
            node2 = node2.next
        else:
            node2 = node2.next
    while node1 is not None:
        if start is None:
            tmp = PostNode(node1.doc, 0, node1.car, node1.title, node1.term)
            start = tmp
        else:
            tmp.next = PostNode(node1.doc, 0, node1.car, node1.title, node1.term)
            tmp = tmp.next
        node1 = node1.next
    #start.selfZonePrint()
    return start

def ZONEAND(node1, node2):
    ans = None
    rt = None
    while node1 is not None and node2 is not None:
        if node1.doc < node2.doc:
            node1 = node1.next
        elif node1.doc > node2.doc:
            node2 = node2.next
        else:
            if ans is None:
                ans = PostNode(node1.doc, 0, max(node2.car, node1.car), max(node1.title, node2.title),
                               max(node1.term, node2.term))
                rt = ans
            else:
                ans.next = PostNode(node1.doc, 0, max(node2.car, node1.car), max(node1.title, node2.title),
                               max(node1.term, node2.term))
                ans = ans.next
            node2 = node2.next
            node1 = node1.next
    #rt.selfZonePrint()
    return rt

def ZONEOR(node1,node2):
    ans = None
    rt = None
    while node1 is not None and node2 is not None:
        if node1.doc < node2.doc:
            if ans is None:
                ans = PostNode(node1.doc, 0, node1.car, node1.title, node1. term)
                rt = ans
            else:
                ans.next = PostNode(node1.doc, 0, node1.car, node1.title, node1.term)
                ans = ans.next
            node1 = node1.next
        elif node1.doc > node2.doc:
            if ans is None:
                ans = PostNode(node2.doc, 0, node2.car, node2.title, node2. term)
                rt = ans
            else:
                ans.next = PostNode(node2.doc, 0, node2.car, node2.title, node2.term)
                ans = ans.next
            node2 = node2.next
        else:
            if ans is None:
                ans = PostNode(node1.doc, 0, max(node2.car, node1.car), max(node1.title, node2.title),
                               max(node1.term, node2.term))
                rt = ans
            else:
                ans.next = PostNode(node1.doc, 0, max(node2.car, node1.car), max(node1.title, node2.title),
                                    max(node1.term, node2.term))
                ans = ans.next
            node2 = node2.next
            node1 = node1.next
    while node1 is not None:
        if ans is None:
            ans = PostNode(node1.doc, 0, node1.car, node1.title, node1.term)
            rt = ans
        else:
            ans.next = PostNode(node1.doc, 0, node1.car, node1.title, node1.term)
            ans = ans.next
        node1 = node1.next
    while node2 is not None:
        if ans is None:
            ans = PostNode(node2.doc, 0, node2.car, node2.title, node2.term)
            rt = ans
        else:
            ans.next = PostNode(node2.doc, 0, node2.car, node2.title, node2.term)
            ans = ans.next
        node2 = node2.next
    #rt.selfZonePrint()
    return rt
#运算符优先级
def ZoneCompare(op1, op2):
    return op1 in ["AND", "ANDNOT"] and op2 in ["OR", "ORNOT"]

#运算
def ZoneGetvalue(num1, num2, operator):
    if operator == "AND":
        return ZONEAND(num1,num2)
    elif operator == "ANDNOT":
        return ZONEANDNOT(num1,num2)
    elif operator == "OR":
        return ZONEOR(num1,num2)
    else:
        print('illegal Operation')
        return None

#出栈入栈
def ZoneProcess(data, opt):
    operator = opt.pop()
    num2 = data.pop()
    num1 = data.pop()
    data.append(ZoneGetvalue(num1, num2, operator))

#查询答案
def ZoneSearch(query,model):
    s=query.split(' ')
    if len(s)==1:
        one=getZoneNode(s[0],model)
        if one!=None:
            one.selfZonePrint()
        else:
            print('None')
        return one
    # i=0
    # flag=True
    # multi=[]
    # while i<len(s):
    #     if i%2==1 and s[i]!='AND':
    #         flag=False
    #     elif i%2==0:
    #         multi.append(s[i])
    #     i+=1
    # if flag:
    #     temp=[]
    #     for t in multi:
    #         if t not in termDic:
    #             print('term error: ',t)
    #             return None
    #         temp.append(termDic[t])
    #     return MULTIAND(temp)
    operator='ORANDNOT()'
    data = []  # 数据栈
    opt = []  # 操作符栈
    i = 0  # 表达式遍历索引
    while i < len(s):
        if s[i] not in operator:  # 入栈data
            node=getZoneNode(s[i],model)
            if node==None:
                print('NO term!:',s[i])
                return None
            data.append(node)
        elif s[i] == ")":  # 右括号，opt出栈同时data出栈并计算，计算结果入栈data，直到opt出栈一个左括号
            while opt[-1] != "(":
                ZoneProcess(data, opt)
            opt.pop()  # 出栈"("
        elif not opt or opt[-1] == "(":  # 操作符栈为空，或者操作符栈顶为左括号，操作符直接入栈opt
            opt.append(s[i])
        elif s[i] == "(" or ZoneCompare(s[i], opt[-1]):  # 当前操作符为左括号或者比栈顶操作符优先级高，操作符直接入栈opt
            opt.append(s[i])
        else:  # 优先级不比栈顶操作符高时，opt出栈同时data出栈并计算，计算结果如栈data
            while opt and not ZoneCompare(s[i], opt[-1]):
                if opt[-1] == "(":  # 若遇到左括号，停止计算
                    break
                ZoneProcess(data, opt)
            opt.append(s[i])
        i += 1  # 遍历索引后移
    while opt:
        ZoneProcess(data, opt)
    result=data.pop()
    if result!=None:
        result.selfZonePrint()
        return result
    return None
