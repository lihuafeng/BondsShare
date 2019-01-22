# -*- coding: utf-8 -*-
"""
@author: lihuafeng
"""

# 动态网站数据爬取

from selenium import webdriver
import pandas as pd

list_url = "http://www.sse.com.cn/market/stockdata/dividends/dividend/"
url = "http://www.sse.com.cn/assortment/stock/list/info/profit/index.shtml?COMPANY_CODE=600660"

# 导出
def parse_Equity_registers(aObj):
    # parse len
    objlen = len(aObj)
    if objlen > 2:
        str1 = [] # 股权登记日
        str2 = [] # 股权登记日总股本(万股)
        str3 = [] # 除息交易日
        str4 = [] # 除息前日收盘价
        str5 = [] # 除息报价
        str6 = [] # 每股红利  含税
        str7 = [] # 每股红利 除税
        str8 = [] #每股 分红率
        for i in range(2,objlen):
            line = aObj[i].text.split("\n")
            str1.append(line[0])
            str2.append(line[1])
            str3.append(line[2])
            str4.append(line[3])     
            str5.append(line[4])
            str6.append(line[5])
            str7.append(line[6])
            if "-" in line[6]:
                str8.append("")
            else:
                str8.append( str(round(float (line[6]) / float (line[4])*100,2))+"%" )
        str1.append("")
        str2.append("")
        str3.append("")
        str4.append("")
        str5.append("")
        str6.append("")
        str7.append("")
        str8.append("")
        Equity_registers = pd.DataFrame({"股权登记日":str1,
                                         "股权登记日总股本(万股)":str2,
                                         "除息交易日":str3,
                                         "除息前日收盘价":str4,
                                         "除息报价":str5,
                                         "每股红利含税":str6,
                                         "每股红利除税":str7,
                                         "分红率":str8},columns = ["股权登记日","股权登记日总股本(万股)","除息交易日","除息前日收盘价","除息报价","每股红利含税","每股红利除税","分红率"])
        return Equity_registers
    
# 抓取
def bonus_spider(url,num):
    try:
        obj.set_page_load_timeout(5)
        obj.get(url)
        obj.implicitly_wait(10)
        # print(obj.title)
        a = obj.find_elements_by_xpath('//*[@id="tableData_one"]/div[2]/table/tbody/tr')
        adf = parse_Equity_registers(a)
        # print(adf)
        adf.to_csv("data/"+num + ".csv", encoding="gb2312")
        obj.quit()
    except Exception as e:
        print(e)
obj = webdriver.PhantomJS(executable_path="E:\MyPython\phantomjs.exe")
try:
    # 抓取列表
    obj.get(list_url)
    obj.implicitly_wait(10)
    list = obj.find_elements_by_xpath('//*[@id="tableData_"]/div[2]/table/tbody/tr/td')

    for i,v in enumerate(list):
       if i is 0:
           num = v.text
           detail_url = "http://www.sse.com.cn/assortment/stock/list/info/profit/index.shtml?COMPANY_CODE=%s" % num
           bonus_spider(detail_url,num)
    obj.quit()
except Exception as e:
    print(e)
