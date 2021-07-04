# coding=utf-8
from os import link, name
from bs4.element import NamespacedAttribute
import requests
import re
from bs4 import BeautifulSoup
import os

mangadoge_search = 'https://dogemanga.com/?q='
links = []#搜索时找到的链接
texts = []#搜索找到的标题
    

def manga_details(lnk):#漫画详细页面
    print('正在获取漫画详细页面... Now Loading...')
    print(':::manga details page:::')
    dtl_dkmt = requests.get(lnk).text #detail document 详细文档
    aftdoc = BeautifulSoup(dtl_dkmt,"html.parser")
    manga_Mtitle = aftdoc.find_all('h2',class_="site-red-dot-box")#漫画 大标题
    name1 = []#不得不说这真的麻烦
    name2 = []
    name3 = ''
    zzbds1 = re.compile(r'[\S.*]+')
    for i in manga_Mtitle:
        name1.append(i.get_text())
    for ii in range(len(name1)):
        name2.extend(zzbds1.findall(name1[ii]))
    for iii in range(len(name2)):
        name3 = name3 + name2[iii]
    print('漫画标题:' + name3)#都是为了提取标题

    manga_details_info = aftdoc.find_all('p',class_="lead text-truncate mt-3")#漫画简介
    jianjie = []
    jianjie1 = ''
    for it in manga_details_info:
        jianjie.append(it.get_text())
    for it1 in range(len(jianjie)):
        jianjie1 = jianjie1 + jianjie[it1]
    print('漫画简介:' + jianjie1)#简介

    print('--章节------------------')
    hua = aftdoc.find_all('option')
    hua_title = []
    hua_links = []
    total_hon = 0
    for boynextdoor in hua:
        hua_title.append(boynextdoor.get_text())
        hua_links.append(boynextdoor['value'])
    for asswecan in range(len(hua_title)):
        print(str(asswecan) + ':' + str(hua_title[asswecan]))
        total_hon = total_hon + 1
    #print('test::::',hua_links)
    print('共有' + str(total_hon) + '个章节')
    input1 = int(input('请输入序号,来进行下载:'))
    manga_download(hua_links[input1],hua_title[input1],name3)

def manga_download(link,hua,title):
    print('::::::Download::::::')
    if not os.path.exists("img"):
        os.mkdir("img")
    res = re.compile(r'\S+')
    hua1 = res.findall(hua)
    hua2 = ''
    for i1 in range(len(hua1)):
        hua2 = hua2 + str(hua1[i1])
    if not os.path.exists("img/" + title +"/"):
        os.mkdir("img/" + title +"/" )
    if not os.path.exists("img/" + title +"/"+ str(hua2)):
        os.mkdir("img/" + title +"/"+ str(hua2))
    page = requests.get(link).text
    res1 = re.compile(r'"(https://dogemanga.com/images/pages/.+?.jpg)"')
    reg = re.findall(res1,page)
    num = 0
    for i in reg:
        a = requests.get(i)
        f = open("img/" + title +"/"+ str(hua2)+"/" + "%s.jpg"%num,'wb')
        f.write(a.content)
        f.close()
        print('第' + str(num) +'页',"下载完了...")
        num = num + 1




if __name__ == '__main__':
    print('欢迎使用漫画狗自动爬图脚本 图源:dogemanga.com!\nscript by Reiz    ver1.0')
    manga_name = input("请输入你想要看的漫画名(关键字):")
    reseach_content = requests.get(mangadoge_search+manga_name).text
    print('你现在正在搜索的是:%s'%manga_name)
    soup = BeautifulSoup(reseach_content,"html.parser")
    search_results = soup.find_all('a',class_="site-red-dot-box site-link")
    
    afttxts = [] #处理后文本
    zzbds = re.compile(r'[\s\S.*]+')
    manga_count = 0
    for i in search_results:
        links.append(i['href'])
        texts.append(i.get_text())

    for inte in range(len(texts)):
        afttxts.extend(zzbds.findall(texts[inte]))
    print('下面是找到的所有结果!')
    
    for ii in range(len(afttxts)):
       print(str(ii) + ":" + afttxts[ii])
       manga_count = ii
    print(':总共搜到了::::' , manga_count,'部漫画')
    select1 = int(input('请输入你想选择的漫画:'))
    if select1 < 0 or select1 > manga_count:
        print('你写错了')
    else:
        #print(select1,'选中的链接:' , links[select1])
        print('你选中了:' + str(select1) + ':::')
        manga_details(links[select1])


    print('-------------------------END---------------------')
    #for num in range(len(links)):
     #   print(links[num])


