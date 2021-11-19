# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 11:48:06 2021

@author: Gagan B K
"""
# Import necessary packages
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
from selenium import webdriver

data = []

month = (['2019/January/','2019/February/','2019/March/','2019/April/','2019/May/','2019/June/','2019/July/','2019/August/','2019/September/','2019/October/','2019/November/','2019/December/','2020/January/','2020/February/','2020/March/','2020/April/','2020/May/','2020/June/','2020/July/','2020/August/','2020/September/','2020/October/','2020/November/','2020/December/','2021/January/','2021/February/','2021/March/','2021/April/','2021/May/','2021/June/','2021/July/','2021/August/','2021/September/'])

# Site URL
URL ="https://www.poultrybazaar.net/daily-rate-sheet/Broiler-Rates-Andhra-Pradesh/"

#define a function
def scrap(month): 
    url=URL+str(month)
    html_content = requests.get(url).text # Make a GET request to fetch the raw HTML content
    soup = BeautifulSoup(html_content, "html.parser")# Parse HTML code for the entire site
    print(soup.prettify()) # print the parsed data of html
    table = soup.find('table', {"class" : "table"})
    try:
# loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)
         for row in table.find_all('tr'):
             cols = row.find_all('td')
             if len(cols) == 34:
                data.append((cols[0].text.strip(), cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip(),cols[5].text.strip(),cols[6].text.strip(),cols[7].text.strip(),cols[8].text.strip(),cols[9].text.strip(),cols[10].text.strip(),cols[11].text.strip(),cols[12].text.strip(),cols[13].text.strip(),cols[14].text.strip(),cols[15].text.strip(),cols[16].text.strip(),cols[17].text.strip(),cols[18].text.strip(),cols[19].text.strip(),cols[20].text.strip(),cols[21].text.strip(),cols[22].text.strip(),cols[23].text.strip(),cols[24].text.strip(),cols[25].text.strip(),cols[26].text.strip(),cols[27].text.strip(),cols[28].text.strip(),cols[29].text.strip(),cols[30].text.strip(),cols[31].text.strip(),cols[32].text.strip()))
    except: pass  


# Data Extraction

for i in month:
    print("Extracting Month-->",i)
    scrap(i)

#New dataframe created

df=pd.DataFrame(data)
data2=pd.DataFrame()

# Label Encoder

from sklearn.preprocessing import LabelEncoder

# creating instance of labelencoder

labelencoder = LabelEncoder()
df["seq"]=labelencoder.fit_transform(df[0])

b=[0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]

for i in b :
    df = df.drop(df[df.seq == i].index) 

df.reset_index(inplace = True)  
b= [7,9,11,13,15,17,19,21,23,25,27,29,32,33,35,36,38,39,41,42,44,45,47,48,50,51,53,54,56,57,59,60,62,63,65,66,68,69,71,72]
df=df.drop(df.iloc[b,:].index)

df=df.reset_index()

for i in list(range(0,33)):
   array=np.asarray(df.iloc[i,3:-1])
   array=list(array)
   data2=(data2.append(array))

print(data2)

data2.columns=["Rates"]
data2=data2.reset_index()
droplist=[59,60,61,123,185,278,340,432,433,495,557,650,712,803,804,805,867,929]

for i in droplist:
    data2=data2.drop(i)
data2=data2.reset_index()   

time = datetime.datetime.now()
time=time.strftime("%d-%m-%y")
length=pd.date_range(start='1/1/2019',end= time , freq='D')
data2=data2.iloc[:len(length),2:]

data2['Date'] = pd.date_range(start='1/1/2019',end= time , freq='D')


data2.columns

data2 = data2.rename(columns={0: 'Rates'})


data2=data2[['Date','Rates']]

data2.to_csv('F:\\Project\\Team 2 files\\complete.csv',index=False)
df=pd.read_csv('F:\\Project\\Team 2 files\\complete.csv')
driver = webdriver.PhantomJS("C:\\Users\\hp\\selenium driver\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")

driver.get('http://www.tsapbcc.com/')
path = '/html/body/div[3]/div/div[2]/div[2]/div/section/ul/li[5]/table/tbody/tr[4]/td[2]'
rates=driver.find_element_by_xpath(path).text
rates=float(rates)
rates=int(rates)

df.iloc[-1, df.columns.get_loc('Rates')] = rates
df['Rates'].iloc[930]=139

df.to_csv('F:\\Project\\Team 2 files\\ARIMA complete.csv', index=False)

df =pd.read_csv(r"F:\\Project\\Team 2 files\\ARIMA complete.csv")

df.columns
df.describe()
df.isna().sum() # to check total NAs
df = df.fillna(df.mean()) # replace NA values with mean value 
df.isna().sum()

sns.boxplot(df["Rates"])

sns.distplot(df["Rates"])

import pandas as pd
import statsmodels.graphics.tsaplots as tsa_plots
from statsmodels.tsa.arima.model import ARIMA


tsa_plots.plot_acf(df.Rates, lags = 7)
tsa_plots.plot_pacf(df.Rates,lags = 7)

# ARIMA with MA = 7
model1 = ARIMA(df.Rates, order = (1,1,7))
res1 = model1.fit()
print(res1.summary())


p=1
q=0
d=1

pdq=[]
for q in range(7):
    try:
        model = ARIMA(df.Rates, order = (p, d, q))
        x1= p,d,q
        pdq.append(x1)
    except:
        pass
            
keys = pdq


# one-step out of sample forecast
start_index = len(df)
end_index = len(df)

# Forecast next 1 day value
forecast = res1.predict(start=start_index, end=end_index)

print('Forecast: %f' % forecast)


# Forecast for next 7 days
start_index = len(df)
end_index = start_index + 6
forecast = res1.predict(start=start_index, end=end_index)

print(forecast)

