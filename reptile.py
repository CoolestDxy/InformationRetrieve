import requests
from bs4 import BeautifulSoup
import re
import random
import time


def getArticle(carNum):
    # 设置目标url，使用requests创建请求
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
    url = 'http://newcar.xcar.com.cn/' + carNum + '/news.htm'
    req = requests.get(url=url, headers=header)
    req.encoding = "gb18030"  # 解决乱码问题
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    linkList = soup.findAll('p', class_="post_tt")
    carTitle=soup.find('div', class_="tt_h1")
    carName=carTitle.find('span', class_="lt_f1").get_text()+carTitle.find('h1').get_text()
    for i in range(5):
        c=linkList[i]
        info=c.find('a')
        subUrl='http:'+info['href']
        title=info['title']
        req = requests.get(url=subUrl, headers=header)
        contents = BeautifulSoup(req.text, "html.parser").find('div', class_="artical_player_wrap").stripped_strings
        s=''
        for c in contents:
            s+=c
        with open('corpus/'+carName+'_'+title.replace(' ','').replace('/',')'),'w',encoding='utf-8')as file:
            file.write(s)

cars=[]
count=0
with open('carNum','r')as file:
    for line in file:
        cars.append(line[:-2])
for i in range(len(cars)):
    count+=1
    print(count)
    try:
        getArticle(cars[i])
    except:
        print('error')
    time.sleep(random.uniform(1, 3))

