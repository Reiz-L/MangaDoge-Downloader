# coding=utf-8
from typing import Text
from bs4.element import NamespacedAttribute
import requests
import re
from bs4 import BeautifulSoup
import os
import platform

#更新功能 未来版本预计更新一次性下载所有话的功能,此版本更新可以二次搜索的功能，伪装UA,重写搜索功能,完美兼容Windows,Linux

#全局变量表
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59'
}#模拟浏览器UA
fake = 'deepdark'#混淆参数？
param = {
    'query':fake#参数
}
manga_name = '' #漫画名称
search_content = '' #搜索页面的html内容
soup = None #soup要分析的
search_results = None #搜索结果
zzbds = re.compile(r'[\s\S.*]+') #要用的正则表达式
aftext = []#处理后的文本集合
mangadoge_search = 'https://dogemanga.com/?q='#搜索前缀
links = []#搜索时找到的链接
texts = []#搜索找到的标题
nextPageButton = None#下一页的按钮
nextPageButton_link = ''#下一页按钮的链接


def manga_search(name):
    search_content = requests.get(url=mangadoge_search+name,params=param,headers=header).text
    print('你现在正在搜索的是:%s'%name)
    soup = BeautifulSoup(search_content,"html.parser")
    search_results = soup.find_all('a',class_="site-red-dot-box site-link")
    manga_count = 0
    for i in search_results:
        links.append(i['href'])
        texts.append(i.get_text())
    if len(texts) >= 13:
        nextPageButton = soup.find_all('a',class_="btn btn-primary btn-lg")
        temp = []
        for i in nextPageButton:
            temp.append(i['href'])
        nextPageButton_link = temp[0]
    for i in range(len(texts)):
        aftext.extend(zzbds.findall(texts[i]))
    print('下面是找到的所有结果!')
    for i in range(len(aftext)):
        print(str(i)+':'+aftext[i])
        manga_count = manga_count + 1
    manga_count = manga_count - 1
    if len(aftext) >= 13:
        print('13:\n下一页 输入0可以返回上级')
    print('::::共找到' + str(manga_count) + '个结果::')
    while True:
        input1 = int(input('请选择序号:'))
        #print('code block 1')
        if input1 == 13 and len(aftext) >=13:
            search_content = requests.get(url=nextPageButton_link,params=param,headers=header).text
            soup = BeautifulSoup(search_content,"html.parser")
            search_results = soup.find_all('a',class_="site-red-dot-box site-link")
            links.clear()
            texts.clear()
            aftext.clear()
            manga_count = 0
            for i in search_results:
                links.append(i['href'])
                texts.append(i.get_text())
            if len(texts) >= 13:
                nextPageButton = soup.find_all('a',class_="btn btn-primary btn-lg")
                temp1 = []
                for i in nextPageButton:
                    temp1.append(i['href'])
                nextPageButton_link = temp1[0]
                #print('code block 2')
            for i in range(len(texts)):
                aftext.extend(zzbds.findall(texts[i]))
            print('以下是找到的所有结果!')
            for i in range(len(aftext)):
                print(str(i) + ':' + aftext[i])
                manga_count = i
            if len(aftext) >= 13:
                print('13:\n下一页 输入0即可返回上一级')
            print('::::共找到' + str(manga_count) + '个结果::')
        elif input1 > 0:
            manga_details(links[input1])
            print('\n\n\n\n\n\n\n\n\n')
            print('下面是找到的所有结果!')
            for i in range(len(aftext)):
                print(str(i)+':'+aftext[i])
                manga_count = i
            manga_count = manga_count - 1
            if len(aftext) >= 13:
                print('13:\n下一页 输入0可以返回上级')
            print('::::共找到' + str(manga_count) + '个结果::')
        elif input1 == 0:
            links.clear()
            texts.clear()
            aftext.clear()
            manga_count = 0
            if platform.system() == "Windows":
                os.system("cls")
            elif platform.system() == "Linux":
                os.system("clear")
            break

def manga_details(lnk):
    print('正在获取漫画详细页面... Now Loading...')
    print('::提示输入1919810可以订阅,输入514810取消订阅::::')
    print(':::manga details page:::')
    dtl_dkmt = requests.get(url=lnk,params=param,headers=header).text #detail document 详细文档
    aftdoc = BeautifulSoup(dtl_dkmt,"html.parser")
    manga_Mtitle = aftdoc.find_all('h2',class_="site-red-dot-box")#漫画 大标题
    name1 = []#不得不说这真的麻烦
    name2 = []
    name3 = ''
    zzbds1 = re.compile(r'[\S.*]+')
    for i in manga_Mtitle:
        name1.append(i.get_text())
    for i in range(len(name1)):
        name2.extend(zzbds1.findall(name1[i]))
    for i in range(len(name2)):
        name3 = name3 + name2[i]
    print('漫画标题:' + name3)#都是为了提取标题
    manga_details_info = aftdoc.find_all('p',class_="lead text-truncate mt-3")#漫画简介
    jianjie = []
    jianjie1 = ''
    for it in manga_details_info:
        jianjie.append(it.get_text())
    for it1 in range(len(jianjie)):
        jianjie1 = jianjie1 + jianjie[it1]
    print('漫画简介:' + jianjie1)#简介
    #获取订阅状态
    if os.path.exists('sub.txt'):
        f = open('sub.txt','r')
        txt1 = f.read()
        f.close()
        if name3 in txt1:
            print('|订阅状态:已订阅|')
        else:
            print('|订阅状态:还没有订阅|')
    else:
        print('|你没有订阅这部本|')
    #订阅结束
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
    while True:
        print('共有' + str(total_hon) + '个章节')
        input1 = int(input('请输入序号来进行下载,输入114514返回上一级:'))
        if input1 == 114514:
            break
        elif input1 == 1919810:#订阅
            if os.path.exists('sub.txt'):
                fr = open('sub.txt','r')
                if name3 in fr.read():
                    print('你已经订阅了这本本子了哦')
                    fr.close()
                else:
                    fr.close()
                    f = open('sub.txt','r')
                    data = f.read().split('\n')
                    f.close()
                    data.append(name3 + '|' + lnk+';')
                    exp = re.compile(r'\S+')
                    dat = []
                    for i in range(len(data)):
                        dat.extend(exp.findall(data[i]))
                    f1 = open('sub.txt','w')
                    for i in dat:
                        f1.write(i)
                    f1.close()
                    print('已订阅!')
            else:
                f1 = open('sub.txt','w')
                f1.write(name3 + '|' + lnk + ';')
                f1.close()
                print('已订阅!')
        elif input1 == 514810:#取消订阅
            if os.path.exists('sub.txt'):
                flread = open('sub.txt','r')
                if name3 in flread.read():
                    flread.close()
                    read1 = open('sub.txt','r')
                    dat = read1.read()
                    read1.close()
                    fg = dat.split(';')
                    r2 = open('sub.txt','w')
                    mh = None
                    for i in fg:
                        if name3 in i:
                            mh = True
                        if not name3 in i:
                            if mh == True:
                                r2.write(i)
                            else:
                                r2.write(i+';')
                    r2.close()
                    print('已取消订阅!')
                else:
                    flread.close()
                    print('没订阅取消什么呢?')
            else:
                print('没有订阅要怎么取消呢?')
        elif input1 < 114514:
            manga_downloader(hua_links[input1],hua_title[input1],name3)
            if platform.system() == "Windows":
                os.system("cls")
            elif platform.system() == "Linux":
                os.system("clear")
            print('::下载已完成:::')
            print('漫画标题:' + name3)
            print('漫画简介:' + jianjie1)#简介
            print('--章节------------------')
            for i in range(len(hua_title)):
                print(str(i)+ ':' + str(hua_title[i]))

    

def manga_downloader(link,hua,title):
    print('::::::Download::::::')
    print('-开始下载 ' + title + hua + '-')
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


#主函数
if __name__ == '__main__':
    print('欢迎使用漫画狗自动爬图脚本 图源:dogemanga.com!\nscript by Reiz')
    help = '输入/exit来退出程序\n/settings来设置程序\n/version来查看版本\n/sr 关键字 来进行搜索\n/help 来获取帮助\n/cls来清屏\n/sub来查看订阅\n/mrtj 每日推荐'#帮助文本
    print(help)
    while True:
        command = input('请输入指令:')
        if ('/sr' in command):
            data1 = command.split()
            manga_name = data1[1]
            manga_search(manga_name)
            #print(manga_name)
            #break
        elif command == '/exit':
            break
        elif command == '/settings':
            print('目前仅能设置用来伪装的UA,请你输入你想伪装用的UA')
            input_UA = str(input('请输入:'))
            if input_UA != '':
                header = {
                'User-Agent':input_UA
                }
                print('设置成功!')
        elif command == '/version':   
            print('----VERSION---------')
            print('当前版本为 1.2\n更新内容为:新增订阅和每日推荐(只推荐Reiz喜欢的东西\n更新日期为2021/7/4\n最初的1.0版本 制作日期为2021/7/1\n    script by Reiz')
            print('--------------------')
        elif command == '/help':
            print(help)
        elif command == '/cls':
            if platform.system() == "Windows":
                os.system("cls")
            elif platform.system() == "Linux":
                os.system("clear")
        elif command == '/sub':
            print('你订阅了:')
            if os.path.exists('sub.txt'):
                try:
                    sub_file = open('sub.txt','r')
                    print('文件读取成功!\n:::订阅Sub::::::')
                    sub = sub_file.read()
                    sub_file.close()
                    sub_fg = sub.split(';')
                    #print(sub_fg)
                    sub_txt = []
                    aft_sub_titles = []
                    aft_sub_links = []
                    for i in sub_fg:
                        if i != '':
                            sub_txt.append(i)
                    #print(sub_txt)
                    for i in range(len(sub_txt)):
                        temp = sub_txt[i]
                        temp1 = temp.split('|')
                        aft_sub_titles.append(temp1[0])
                        aft_sub_links.append(temp1[1])
                    #print(aft_sub_titles,aft_sub_links)
                    for i in range(len(aft_sub_titles)):
                        print(str(i)+':'+aft_sub_titles[i])
                    while True:
                        inp = int(input('输入你要打开的订阅(114514返回):'))
                        if inp < 0 or inp > 114514:
                            print('超出范围!请重新输入!')
                        elif inp < 114514 and inp >= 0:
                            manga_details(aft_sub_links[inp])
                            print('::订阅Sub:::::')
                            sub_file = open('sub.txt','r')
                            sub = sub_file.read()
                            sub_file.close()
                            sub_fg = sub.split(';')
                            
                            sub_txt.clear()
                            aft_sub_titles.clear()
                            aft_sub_links.clear()
                            for i in sub_fg:
                                if i != '':
                                    sub_txt.append(i)
                            for i in range(len(sub_txt)):
                                temp = sub_txt[i]
                                temp1 = temp.split('|')
                                aft_sub_titles.append(temp1[0])
                                aft_sub_links.append(temp1[1])
                            for i in range(len(aft_sub_titles)):
                                print(str(i)+':'+aft_sub_titles[i])
                        elif inp == 114514:
                            print('返回...')
                            break
                except Exception as e:
                    print('获取订阅失败了!错误如下:')
                    print(e)
            else:
                print('你还没订阅任何东西哟~')
        elif command == '/mrtj':
            print('无法连接到服务器，获取数据失败!')

    print('已退出程序...')
        

