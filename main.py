# -*- coding: utf-8 -*-
"""
Created on Tue May 26 22:46:53 2020

@author: pjpf8
"""

from function import *  #從function中import全部資料
import pandas as pd
import requests, sys, csv
from bs4 import BeautifulSoup
import os
import selenium,time,re,requests
from selenium import webdriver
import time as tm
from random import randint

userchoose = input("請選擇想搜尋的項目:(1)課名，(2)教師，(3)教師 + 課名: ")  #讓使用者選擇要使用哪種關鍵字搜尋課程貼文內容

if userchoose == "1":      #如果選擇課名
    target = input("請輸入想搜尋的課名: ")
    time = input("請輸入想搜尋到的年份: ")
    url="https://www.ptt.cc/bbs/NTHU_Course/index.html"
    for page in range(1,100):
        #先取PTT資料
        r = requests.get(url)  #利用requset取得網頁資料
        soup = BeautifulSoup(r.text,"html.parser")  #"r.text"(網路原始碼)，"html.parser"(文字解析器)，指定BeautifulSoup用lxml解析網路原始碼
        btn = soup.select('div.btn-group > a')   #從PTT的網頁原始碼中選取<div><btn-group > a>的部分
        up_page_href = btn[3]['href']
        next_page_url = 'https://www.ptt.cc' + up_page_href
        url = next_page_url
        get_all_href(url, target, time)   #利用get_all_href取得PTT貼文資料


    check = checkfile('ptt_' + target + ".csv")  #確認ptt_' + target + ".csv是否已存在
    if check == True:        #若存在，讀取已取得的資料，並印出
        ptt = pd.read_csv('ptt_' + target + ".csv", encoding = "big5")
        pttarticle = ptt['全文'].tolist()
        for i in range(0, len(pttarticle)):
            print("(" + str(i + 1) + ")." + "\n" + pttarticle[i])
     
    else:                  #若不存在，印出查無資料
        print("\n利用您所輸入的關鍵字在PTT查無資料，如需查詢，請更變查詢年份或關鍵字\n")
        
    
    fb = getfacebook(time)  #利用getfacebook()取得FB資料
    fb.pop(0) 
    with open('fb_' + target + '.csv', 'w', encoding = 'utf-8-sig') as csvfile: #將取得的資料存入csv檔
        writer = csv.writer(csvfile)
        writer.writerow(['全文'])
        for i in range(0,len(fb)): 
            if target in fb[i]:
                writer.writerow([fb[i]])
    
    check = checkfile('fb_' + target + '.csv')   #確認fb_' + target + ".csv是否已存在
    if check == True:   #若存在，讀取已取得的資料，並印出
        fb = pd.read_csv('fb_' + target + '.csv', 'w', encoding = 'utf-8-sig')
        fbarticle = fb['全文'].tolist()
        for i in range(0, len(fbarticle)):
            print("\n" + fbarticle[i] + "\n")
            
    else:    #若不存在，印出查無資料
        print("\n利用您所輸入的關鍵字Facebook查無資料，如需查詢，請更變查詢年份或關鍵字\n")
            
    google = getlecture(target) #利用getlecture取得用課名搜尋的google表單資料，並印出
    
    for i in range(0, len(google)):
        print("(" + str(i + 1) + ")." + "\n" + google[i])
    
if userchoose == "2":          #如果選擇教師
    target = input("請輸入想搜尋的教師: ")
    time = input("請輸入想搜尋到的年份: ")
    url="https://www.ptt.cc/bbs/NTHU_Course/index.html"
    for page in range(1,100):
        #先取PTT資料
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        btn = soup.select('div.btn-group > a')
        up_page_href = btn[3]['href']
        next_page_url = 'https://www.ptt.cc' + up_page_href
        url = next_page_url
        get_all_href(url, target, time)

    check = checkfile('ptt_' + target + ".csv")
    if check == True:
        ptt = pd.read_csv('ptt_' + target + ".csv", encoding = "big5")
        pttarticle = ptt['全文'].tolist()
        for i in range(0, len(pttarticle)):
            print("(" + str(i + 1) + ")." + "\n" + pttarticle[i])
     
    else:
        print("\n利用您所輸入的關鍵字在PTT查無資料，如需查詢，請更變查詢年份或關鍵字\n")
    
    fb = getfacebook(time)   #利用getfacebook()取得FB資料
    fb.pop(0)
    with open('fb_' + target + '.csv', 'w', encoding = 'utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['全文'])
        for i in range(0,len(fb)): 
            if target in fb[i]:
                writer.writerow([fb[i]])
    
    check = checkfile('fb_' + target + '.csv')   
    if check == True:
        fb = pd.read_csv('fb_' + target + '.csv', 'w', encoding = 'utf-8-sig')
        fbarticle = fb['全文'].tolist()
        for i in range(0, len(fbarticle)):
            print("\n" + fbarticle[i] + "\n")      
    else:
        print("\n利用您所輸入的關鍵字Facebook查無資料，如需查詢，請更變查詢年份或關鍵字\n")
            
    google = getteacher(target) #利用getteacher取得用課名搜尋的google表單資料，並印出
    
    for i in range(0, len(google)):
        print("(" + str(i + 1) + ")." + "\n" + google[i])

if userchoose == "3":    #如果選擇教師和課名
    target1 = input("請輸入想搜尋的課名: ")
    target2 = input("請輸入想搜尋的教師: ")
    time = input("請輸入想搜尋到的年份: ")
    url="https://www.ptt.cc/bbs/NTHU_Course/index.html"
    for page in range(1,200):
        #先取PTT資料
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        btn = soup.select('div.btn-group > a')
        up_page_href = btn[3]['href']
        next_page_url = 'https://www.ptt.cc' + up_page_href
        url = next_page_url
        get_all_href(url, target1, time)


    check = checkfile('ptt_' + target1 + ".csv")
    if check == True:
        ptt = pd.read_csv('ptt_' + target1 + ".csv", encoding = "big5")
        pttarticle = ptt['全文'].tolist()
        for i in range(0, len(pttarticle)):
            if target2 in pttarticle[i]:
                print("(" + str(i + 1) + ")." + "\n" + pttarticle[i])
     
    else:
        print("\n利用您所輸入的關鍵字在PTT查無資料，如需查詢，請更變查詢年份或關鍵字\n")



    fb = getfacebook(time)   #利用getfacebook()取得FB資料
    fb.pop(0)
    with open('fb_' + target1 + '.csv', 'w', encoding = 'utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['全文'])
        for i in range(0,len(fb)): 
            if target1 in fb[i] and target2 in fb[i]:
                writer.writerow([fb[i]])
            
    check = checkfile('fb_' + target1 + '.csv')   
    if check == True:
        fb = pd.read_csv('fb_' + target + '.csv', 'w', encoding = 'utf-8-sig')
        fbarticle = fb['全文'].tolist()
        for i in range(0, len(fbarticle)):
            print("\n" + fbarticle[i] + "\n")     
    else:
        print("\n利用您所輸入的關鍵字Facebook查無資料，如需查詢，請更變查詢年份或關鍵字\n")
        
    google = getall(target1, target2)   #利用getall取得用課名和課名搜尋的google表單資料，並印出
    
    for i in range(0, len(google)):
        print("(" + str(i + 1) + ")." + "\n" + google[i])

