# -*- coding: utf-8 -*-
"""
Created on Mon May 11 22:30:57 2020

@author: boyan
"""
import requests

from bs4 import BeautifulSoup

#抓網址檔案
res = requests.get("https://www.coingecko.com/price_charts/1/twd/90_days.json")
res180 = requests.get("https://www.coingecko.com/price_charts/1/twd/180_days.json")
#res.encoding="UTF-8"
soup = BeautifulSoup(res.text ,'html.parser')
soup180 = BeautifulSoup(res180.text ,'html.parser')

bitPrice=soup.prettify('utf-8').decode('utf-8')
bit180=soup180.prettify('utf-8').decode('utf-8')



#把不要的切掉
import re
m=re.search('{"stats":(.*?),"',bitPrice)
m180=re.search('{"stats":(.*?),"',bit180)

#轉成字典
import json 
jd=json.loads(m.group(1))
jd180=json.loads(m180.group(1))

#轉一維表格
import pandas 
df=pandas.DataFrame(jd)
df180=pandas.DataFrame(jd180)
pandas.set_option('display.max_rows', None)

df.columns=['datetime','twd']
df180.columns=['datetime','twd']

df['datetime']=(df['datetime']//1000*1000)+3600000*8#去尾數

df['datetime']=pandas.to_datetime(df['datetime'],unit='ms')
df180['datetime']=pandas.to_datetime(df180['datetime'],unit='ms')


#df.index=df['datetime']
#print(df180)

#圖表
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import time

#df['twd'].plot(kind='line', figsize=[6,3])

#df['ma7']=df['twd'].rolling(window=7).mean() #七天均線

#df[['twd','ma7']].plot(kind='line',figsize=[6,3])#放兩條線

#只畫指定時後
#df2=df[df['datetime']>='2020-04-01']
#df2[['twd','ma7']].plot(kind='line',figsize=[6,3]) 

#plt.show()

#ui


from tkinter import*

window = Tk()
btnPress=False

def btnPress():      
    plt.close()
    if xyCheck.get()==True:
        plt.grid()
    PicNormal()    
  
def btnHalf():   
    plt.close()
    if xyCheck.get()==True:
        plt.grid()
    PicHalf()
    
def radioPress():
    plt.close()
    if xyCheck.get()==True:
        plt.grid()
    i=radiovalue.get()
    if i==0:
        if bollinger.get()==True:
            PicWeek_bollinger() 
        else:
            PicWeek()
    if i==1:
        if bollinger.get()==True:
            PicMonth_bollinger()
        else:
            PicMonth()


def PicHalf():    
    plt.plot(df180['datetime'],df180['twd'])
    plt.title("Half-year chart",loc="left")
    plt.show()
    
def PicNormal():
    plt.plot(df['datetime'],df['twd'])
    plt.title("Three-month chart",loc="left")
    plt.show()
    
def PicWeek():    
    plt.plot(df['datetime'],df['twd'])
    plt.plot(df['datetime'],df['twd'].rolling(window=24*7).mean())
    plt.title("Three-month chart-Weekly",loc="left")
    plt.show()

def PicWeek_bollinger():
    plt.plot(df['datetime'],df['twd'])
    plt.plot(df['datetime'],df['twd'].rolling(window=24*7).mean())
    plt.plot(df['datetime'],(df['twd'].rolling(window=24*7).mean())+(2*df['twd'].rolling(window=24*7).std()))
    plt.plot(df['datetime'],(df['twd'].rolling(window=24*7).mean())-(2*df['twd'].rolling(window=24*7).std()))
    plt.title("Three-month chart-Weekly with bollinger",loc="left")
    plt.show()

def PicMonth():
    plt.plot(df180['datetime'],df180['twd'])
    plt.plot(df180['datetime'],df180['twd'].rolling(window=30).mean())
    plt.title("Half-year chart-Monthly",loc="left")
    plt.show()

def PicMonth_bollinger():
    plt.plot(df180['datetime'],df180['twd'])
    plt.plot(df180['datetime'],df180['twd'].rolling(window=30).mean())
    plt.plot(df180['datetime'],(df180['twd'].rolling(window=30).mean())+(2*df180['twd'].rolling(window=30).std()))
    plt.plot(df180['datetime'],(df180['twd'].rolling(window=30).mean())-(2*df180['twd'].rolling(window=30).std()))
    plt.title("Half-year chart-Monthly with bollinger",loc="left")
    plt.show()

def freshText():
    print(str1)
    text1.delete("1.0",END)
    
    i=radioTime.get()
    if i==0:
        if str2.get()!="":
            tempAnd=np.logical_and(df['datetime']>=str1.get(),df['datetime']<=str2.get())
            text1.insert(END,df[tempAnd])
        else:
            text1.insert(END,df[df['datetime']>=str1.get()])
    if i==1:
        if str2.get()!="":
            tempAnd=np.logical_and(df180['datetime']>=str1.get(),df180['datetime']<=str2.get())
            text1.insert(END,df180[tempAnd])
        else:
            tempAnd=np.logical_and(df180['datetime']>=str1.get(),df180['datetime']<=time.strftime("%Y-%m-%d"))
            text1.insert(END,df180[tempAnd])

###################################################
window.title("bitcoin")
window.geometry("800x400")
window.maxsize(800,400)

sbar1 = Scrollbar(window)
label1=Label(window,text="資料庫資料",width=39)
label2=Label(window,text="查詢日期:                             ~",width=20)
label3=Label(window,text="精確準度:                              ",width=20)

text1=Text(window,width = 40,height = 10,wrap = WORD)

lineSet={0:"周線",1:"月線"}
radiovalue=IntVar()
radiovalue.set(0)
temp=320
for i in range(len(lineSet)):
    Radiobutton(window,variable=radiovalue,text=lineSet[i],value=i).place(x=temp,y=90)
    temp+=50

month_year={0:"HOUR",1:"DAY"}
radioTime=IntVar()
radioTime.set(0)
temp=60
for i in range(len(lineSet)):
    Radiobutton(window,variable=radioTime,text=month_year[i],value=i).place(x=temp,y=200)
    temp+=100
    
xyCheck=BooleanVar()
bollinger=BooleanVar()
Checkbutton(window,variable=xyCheck,text="X/Y格子").place(x=320,y=0)
Checkbutton(window,variable=bollinger,text="布林通道").place(x=400,y=0)
    
text1.insert(END,df[["datetime","twd"]])

btn1=Button(window,text="近三個月圖表走勢",command=btnPress) 
btn2=Button(window,text="最近半年圖表走勢",command=btnHalf) 
btn3=Button(window,text="確定",command=radioPress) 
btn4=Button(window,text="確定",command=freshText)


str1=StringVar()
entry1=Entry(window,wid=10,textvariable=str1)
str2=StringVar()
entry2=Entry(window,wid=10,textvariable=str2)

btn1.place(x=320,y=30)
btn2.place(x=320,y=60)
btn3.place(x=430,y=90)


label1.place(x=0,y=0)
label2.place(x=0,y=180)
label3.place(x=0,y=200)

entry1.place(x=60,y=180)
entry2.place(x=150,y=180)
btn4.place(x=230,y=178)


sbar1.place(x=300,y=60)
text1.place(x=0,y=30)


sbar1["command"]=text1.yview
text1["yscrollcommand"]=sbar1.set

window.mainloop()




