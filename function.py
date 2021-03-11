# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:52:26 2020

@author: wl030
"""

import requests, sys, csv
from bs4 import BeautifulSoup
import pandas as pd
import os
import selenium,time,re,requests
from selenium import webdriver
import time as tm
from random import randint

data = []
def get_article_time(article_url, target, time): #取得PTT貼文時間的function
    r = requests.get(article_url) #利用requset取得網頁資料
    soup = BeautifulSoup(r.text, "lxml") #"r.text"(網路原始碼)，"lxml"(文字解析器)，指定BeautifulSoup用lxml解析網路原始碼
    results = soup.select('span.article-meta-value') #從PTT的網頁原始碼中選取<span><article-meta-value>的部分
       
        
    post_time = results[3].text      #取得貼文時間
    post_time = post_time.split(' ')[-1] 
    while int(post_time) >= int(time):   #如果貼文年份大於指定搜尋年份，就retrun True
        return True
        
        
def get_all_href(url, target, time):  #取得PTT全部貼文、時間與留言的function
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")  #"r.text"(網路原始碼)，"html.parser"(文字解析器)，指定BeautifulSoup用parser解析網路原始碼
    results = soup.select("div.title") #從PTT的網頁原始碼中選取<div><title>的部分
    for item in results:
        a_item = item.select_one("a")  #抓取標籤為a的原始碼
        title = item.text
        if a_item:
            article_url = 'https://www.ptt.cc'+ a_item.get('href')  #"href"為原始碼標籤
            if target in title:
                if get_article_time(article_url, target, time) is True: #用get_article)time先確認貼文時間是否符合條件
                    content = get_content(article_url)    #利用get_content取得PTT貼文內容
                    data.append([title, article_url,content])  #將貼文內容與貼文標題形成一個list加入data這個list裡
                else:
                    with open('ptt_' + target + '.csv', 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)  #若搜尋到的貼文時間已經不符合條件，就將data這個list存入csv
                        writer.writerow(['標題', '網址','全文'])
                        for i in range(0,len(data)):        
                            writer.writerow([data[i][0],data[i][1],data[i][2]])
                
def get_content(URL):   #取得PTT貼文的function
    rs = requests.session()  #session為一個模擬登入或是點擊登入的套件
    res = rs.get(URL, verify = False)
    soup = BeautifulSoup(res.text, 'html.parser')
    post = soup.select('.bbs-screen.bbs-content')[0].text  #從PTT的網頁原始碼中選取<bbs-screen.bbs-content>的部分
    return post     #輸出貼文內容


def checkfile(file):   #確認檔案是否存在的function
    check = False
    if os.path.isfile(file):
        check = True  #若存在，輸出True
        
    return check
        

            
def getlecture(lecture_name):  #以"課名"取得excel表單裡的課程資料的function
    pd.set_option('display.unicode.ambiguous_as_wide', True)   # 設置列名與數據對齊
    pd.set_option('display.unicode.east_asian_width', True)
    df1 = pd.read_excel("course.xlsx",index_col= "課名")       #讀取course.xlsx中的資料，選擇column課名與教師
    df2 = pd.read_excel("course.xlsx",index_col= "教師")
    df3 = pd.read_excel("course.xlsx")
    df5 = df3.fillna("無資料")                     #以"無資料"將顯示"nan"的資料取代

    
    data1 = df1.loc[lecture_name]


    lecture = data1[["教師","甜度","Loading","整體推薦度"]]  #我們想顯示的資料

    


    df5 = df5.applymap(str)
    ans = []

    for i in range(0,len(df5)):
        if lecture_name in df5["課名"][i]:                #如果讀取到的課名與輸入條件相同，將資料加入ans這個list
            List1 = "課名：" + df5["課名"][i] + "\n" \
            + "教師：" + df5["教師"][i] + "\n" \
            + "甜度：" + df5["甜度"][i] + "\n"\
            + "Loading:" + df5["Loading"][i] + "\n"\
            + "拿分技巧："+ df5["拿分小技巧(如何獲得更好成績)"][i] + "\n"
            ans.append(List1)

    return ans          

def getteacher(teacher_name):     #以"教師"取得excel表單裡的課程資料的function
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    df1 = pd.read_excel("course.xlsx",index_col= "課名")
    df2 = pd.read_excel("course.xlsx",index_col= "教師")
    df3 = pd.read_excel("course.xlsx")
    df5 = df3.fillna("無資料")



    data2 = df2.loc[teacher_name]


    teacher = data2[["課名","甜度","Loading","整體推薦度"]]


    df5 = df5.applymap(str)
    ans = []

    for i in range(0,len(df5)):
        if teacher_name in df5["教師"][i]:    #如果讀取到的教師與輸入條件相同，將資料加入ans這個list
            List1 = "課名：" + df5["課名"][i] + "\n" \
            + "教師：" + df5["教師"][i] + "\n" \
            + "甜度：" + df5["甜度"][i] + "\n"\
            + "Loading:" + df5["Loading"][i] + "\n"\
            + "拿分技巧："+ df5["拿分小技巧(如何獲得更好成績)"][i] + "\n"
            ans.append(List1)
            
    return ans    #輸出ans

def getall(lecture_name, teacher_name):     #以"課名"與"教師"取得excel表單裡的課程資料的function
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    df1 = pd.read_excel("course.xlsx",index_col= "課名")
    df2 = pd.read_excel("course.xlsx",index_col= "教師")
    df3 = pd.read_excel("course.xlsx")
    df5 = df3.fillna("無資料")


    data1 = df1.loc[lecture_name]
    data2 = df2.loc[teacher_name]

    lecture = data1[["教師","甜度","Loading","整體推薦度"]]
    teacher = data2[["課名","甜度","Loading","整體推薦度"]]

    df5 = df5.applymap(str)
    ans = []

    for i in range(0,len(df5)):
        if (lecture_name in df5["課名"][i]) and  teacher_name in df5["教師"][i]:   #如果讀取到的課名和課名與輸入條件相同，將資料加入ans這個list
            List1 = "課名：" + df5["課名"][i] + "\n" \
            + "教師：" + df5["教師"][i] + "\n" \
            + "甜度：" + df5["甜度"][i] + "\n"\
            + "Loading:" + df5["Loading"][i] + "\n"\
            + "拿分技巧："+ df5["拿分小技巧(如何獲得更好成績)"][i]
            ans.append(List1)
            
    return ans


def getfacebook(time):   #取得facebook貼文資料的function
    collect_comment = pd.DataFrame()   #建立dataframe
    collect_fb = pd.DataFrame()

    chrome_options = webdriver.ChromeOptions() #要事先下載chromedriver這個程式，並用webdriver.ChromeOptions()選擇chromedriver來爬facebook的資料
    
    prefs = {"profile.default_content_setting_values.notifications": 2} #這三段code是為了像我們平常看facebook一樣，點選稍後再登入
    chrome_options.add_experimental_option("prefs",prefs)
    driver=webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
    
    driver.get("https://www.facebook.com/NTHUGe")  #取得網站資料

    post=[]

    soup=BeautifulSoup(driver.page_source,"lxml")   #"driver.page_source"(網路原始碼)，"lxml"(文字解析器)，指定BeautifulSoup用lxml解析網路原始碼

    first=soup.find_all(class_="text_exposed_root")  #從FB的網頁原始碼中選取<text_exposed_root>的部分

    for i in first:
        post.append(i.text)

        timme=soup.find_all("abbr") #從FB的網頁原始碼中選取<abbr>的部分

    Course = []
    real=[]
    for i in timme:
        if i.get("title")!=None:
            real.append(i.get("title"))   



    while real[-1].split(" ")[0]>= (str(time) + "年"):#輸入日期，從今天往前搜尋
        Post = []
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        #點開留言
        Links = []
        post=[]
        soup=BeautifulSoup(driver.page_source,"lxml")
        posts = soup.findAll('div', {'class':'clearfix y_c3pyo2ta3'})
        for i in posts:
            Links.append('https://www.facebook.com' + i.find('a',{'class':'_5pcq'}).attrs['href'].split('?',2)[0])

    
        first = soup.find_all(class_="text_exposed_root")
    
        for post in first:
            Post.append(post.text)
    
       
        #爬貼文時間
        timme=soup.find_all("abbr")
        real=[]
        for i in timme:
            if i.get("title")!=None:
                real.append(i.get("title"))

    driver.close()


    return Post
