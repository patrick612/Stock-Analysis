# -*- coding: utf-8 -*-
"""
Here I have written a code which shows how likely the price of a stock will increase the next day if we pick out the cases
where price increase per trade volume has increased in the past two days
"""
import matplotlib as plt
import pandas as pd
import sqlite3
import numpy as np

class Stockdb:
    def __init__(self, path):
        self.path = path
    
    def getlist_excel(self, excel_path):
        stock_filtered = pd.read_excel(excel_path)
        stock_list1 = stock_filtered['종목코드']
        stock_list = stock_list1.tolist()
        
        stock_list_str = []
        for k in stock_list:
            k = str(k)
            if len(k) == 1:
                k = "00000"+k
            elif len(k) == 2:
                k = "0000"+k
            elif len(k) == 3:
                k = "000"+k
            elif len(k) == 4:
                k = "00"+k
            elif len(k) == 5:
                k = "0"+k
            stock_list_str.append(k)
            stock_list = stock_list_str
        
        return stock_list
            
    def getlist_db(self):
        con1 = sqlite3.connect(self.path)
        cursor = con1.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_list = cursor.fetchall()
        
        table_list_str = []
        for j in table_list:
            string_j = str(j[0])
            table_list_str.append(string_j)
        
        stock_list = table_list_str
        
        return stock_list
    
    """
    #this creates a dictionary which links stock code to desired data in dataframe. See the below example code
    # =============================================================================
    # stock_list = ['003380', '005290']
    # con1 = sqlite3.connect("c://Users//Runner//Data//Stock//Dayprice_kosdaq_filtered.db")
    # stockdata_dict = {}
    # columns = 'dates, open, high, low, close, volume'
    # restrain = 'dates>=20201228'
    # for i in stock_list:
    #     stockdata_dict["{}".format(i)] = pd.read_sql("SELECT {0} FROM '{1}' WHERE {2}".format(columns, i, restrain), con1, index_col=None)
    # print(stockdata_dict)
    # =============================================================================
    #Note that path refers to the file you wish to extract the data, stock list refers to list of stocks that are within the db specified by the path
    #columns refer to columns of data in db table you want, restrain refers to sql statement like: dates >= 20201228 or close = 1500
    #if you want all data without specifying column, use * in column. If you dont want to specify restrain, use 'none'
    #Note that since sql command is done in string, putting a number inside a command may look like a string but when read by the sql program is a number
    # so there must be a ' ' around the stock code as shown by '{1}'. On the other hand, the restrain command like date>=20201228 is a command thus does
    #not need an extra ' ' around it within the string sql command.        
    """

    def create_dict(self, stock_list, columns, restrain):
        con1 = sqlite3.connect(self.path)
        stockdata_dict = {}
        if restrain == 'none':
            for i in stock_list:
                stockdata_dict["{}".format(i)] = pd.read_sql("SELECT {0} FROM '{1}'".format(columns, i), con1, index_col=None)
        else:
            for i in stock_list:
                stockdata_dict["{}".format(i)] = pd.read_sql("SELECT {0} FROM '{1}' WHERE {2}".format(columns, i, restrain), con1, index_col=None)
                
        return stockdata_dict
            

kospi = Stockdb("c://Users//Runner//Data//Stock//Dayprice_kospi_filtered.db")
kospi_list = kospi.getlist_db()
print(kospi_list)
kospi_dict = kospi.create_dict(kospi_list, 'dates, open, high, low, close, volume', 'dates >= 20171010')
print(kospi_dict['006840'])



print(len(kospi_dict['006840']))
print(kospi_dict['006840']['close'].iloc[4])
#how to access row via index -> use iloc
#print(kospi_dict['006840'].iloc[1, :])
# accessing column is done by dataframe.iloc[: , 2] This can be generalized to multiple rows or columns: dataframe.iloc[: , [0,2]]

# =============================================================================
# for i in range(5, 190, 1):
#     score = []
#     if ((kospi_dict['006840']['close'].iloc[i] - kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['close'].iloc[i])/(kospi_dict['006840']['volume'].iloc[i])  
#     > (kospi_dict['006840']['close'].iloc[i+1] - kospi_dict['006840']['close'].iloc[i+2])/(kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['volume'].iloc[i+1])
#     > (kospi_dict['006840']['close'].iloc[i+2] - kospi_dict['006840']['close'].iloc[i+3])/(kospi_dict['006840']['close'].iloc[i+2])/(kospi_dict['006840']['volume'].iloc[i+2])) and (kospi_dict['006840']['high'].iloc[i-1] - kospi_dict['006840']['close'].iloc[i])/(kospi_dict['006840']['close'].iloc[i]) >= 0.01:
#         score.append(1)
#     elif ((kospi_dict['006840']['close'].iloc[i] - kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['close'].iloc[i])/(kospi_dict['006840']['volume'].iloc[i])  
#     > (kospi_dict['006840']['close'].iloc[i+1] - kospi_dict['006840']['close'].iloc[i+2])/(kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['volume'].iloc[i+1])
#     > (kospi_dict['006840']['close'].iloc[i+2] - kospi_dict['006840']['close'].iloc[i+3])/(kospi_dict['006840']['close'].iloc[i+2])/(kospi_dict['006840']['volume'].iloc[i+2])) and (kospi_dict['006840']['high'].iloc[i-1] - kospi_dict['006840']['close'].iloc[i])/(kospi_dict['006840']['close'].iloc[i]) <= 0.01:
#         score.append(-1)
#     else:
#         pass
# =============================================================================
    
# =============================================================================
# for i in range(5, 190, 1):
#     score = []
#     if (kospi_dict['006840']['close'].iloc[i] - kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['close'].iloc[i])/np.log10((kospi_dict['006840']['volume'].iloc[i])) > (kospi_dict['006840']['close'].iloc[i+1] - kospi_dict['006840']['close'].iloc[i+2])/(kospi_dict['006840']['close'].iloc[i+1])/np.log10((kospi_dict['006840']['volume'].iloc[i+1])) and (kospi_dict['006840']['high'].iloc[i-1] - kospi_dict['006840']['close'].iloc[i])/(kospi_dict['006840']['close'].iloc[i]) >= 0.01:
#         score.append('1')
#     elif (kospi_dict['006840']['close'].iloc[i] - kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['close'].iloc[i])/np.log10((kospi_dict['006840']['volume'].iloc[i])) > (kospi_dict['006840']['close'].iloc[i+1] - kospi_dict['006840']['close'].iloc[i+2])/(kospi_dict['006840']['close'].iloc[i+1])/np.log10((kospi_dict['006840']['volume'].iloc[i+1])) and (kospi_dict['006840']['high'].iloc[i-1] - kospi_dict['006840']['close'].iloc[i])/(kospi_dict['006840']['close'].iloc[i]) <= 0.01:
#         score.append('-1')
#     else:
#         pass
# print(score)
# =============================================================================
# =============================================================================
# for i in range(5, 190, 1):
#     score = []
#     if (kospi_dict['006840']['close'].iloc[i] - kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['close'].iloc[i])/(kospi_dict['006840']['volume'].iloc[i]) > (kospi_dict['006840']['close'].iloc[i+1] - kospi_dict['006840']['close'].iloc[i+2])/(kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['volume'].iloc[i+1]):
#         score.append('1')
#     elif (kospi_dict['006840']['close'].iloc[i] - kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['close'].iloc[i])/(kospi_dict['006840']['volume'].iloc[i]) > (kospi_dict['006840']['close'].iloc[i+1] - kospi_dict['006840']['close'].iloc[i+2])/(kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['volume'].iloc[i+1]):
#         score.append('-1')
#     else:
#         pass
# print(score)
# i=5
# print((kospi_dict['006840']['close'].iloc[i] - kospi_dict['006840']['close'].iloc[i+1]))
# print((kospi_dict['006840']['close'].iloc[i] - kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['close'].iloc[i])/(kospi_dict['006840']['volume'].iloc[i]))
# print((kospi_dict['006840']['close'].iloc[i+1] - kospi_dict['006840']['close'].iloc[i+2])/(kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['volume'].iloc[i+1]))
# =============================================================================
#print(score)

# =============================================================================
# for i in range(5, 190, 1):
#     score = []
#     if ((kospi_dict['006840']['close'].iloc[i] - kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['close'].iloc[i])/np.log(kospi_dict['006840']['volume'].iloc[i])  
#     > (kospi_dict['006840']['close'].iloc[i+1] - kospi_dict['006840']['close'].iloc[i+2])/(kospi_dict['006840']['close'].iloc[i+1])/np.log(kospi_dict['006840']['volume'].iloc[i+1])
#     > (kospi_dict['006840']['close'].iloc[i+2] - kospi_dict['006840']['close'].iloc[i+3])/(kospi_dict['006840']['close'].iloc[i+2])/np.log(kospi_dict['006840']['volume'].iloc[i+2])) and (kospi_dict['006840']['high'].iloc[i-1] - kospi_dict['006840']['close'].iloc[i])/(kospi_dict['006840']['close'].iloc[i]) >= 0.01:
#         score.append(1)
#     elif ((kospi_dict['006840']['close'].iloc[i] - kospi_dict['006840']['close'].iloc[i+1])/(kospi_dict['006840']['close'].iloc[i])/np.log(kospi_dict['006840']['volume'].iloc[i])  
#     > (kospi_dict['006840']['close'].iloc[i+1] - kospi_dict['006840']['close'].iloc[i+2])/(kospi_dict['006840']['close'].iloc[i+1])/np.log(kospi_dict['006840']['volume'].iloc[i+1])
#     > (kospi_dict['006840']['close'].iloc[i+2] - kospi_dict['006840']['close'].iloc[i+3])/(kospi_dict['006840']['close'].iloc[i+2])/np.log(kospi_dict['006840']['volume'].iloc[i+2])) and (kospi_dict['006840']['high'].iloc[i-1] - kospi_dict['006840']['close'].iloc[i])/(kospi_dict['006840']['close'].iloc[i]) <= 0.01:
#         score.append(-1)
#     else:
#         pass
# 
# print(score)
# =============================================================================


# =============================================================================
# #code to see the logarithmic price distribution and lograithmic price change distribution
# fig = plt.pyplot.figure()
# log_price_dist = fig.add_subplot(3, 1, 1)
# log_pricechange_dist = fig.add_subplot(3, 1, 2)
# pricechange_dist = fig.add_subplot(3, 1, 3)
# 
# x_price = []
# for i in range(5, 790, 1):
#     x_price_val = np.log(kospi_dict['006840']['close'].iloc[i])
#     x_price_val = round(x_price_val, 2)
#     x_price.append(x_price_val)   
# print(x_price)    
# y_price = [x_price.count(i) for i in x_price]
# print(y_price)
# 
# x_log_pricechange = []
# for i in range(5, 790, 1):
#     x_log_pricechange_val = np.log((kospi_dict['006840']['close'].iloc[i])/kospi_dict['006840']['close'].iloc[i+1])
#     x_log_pricechange_val = round(x_log_pricechange_val, 3)
#     x_log_pricechange.append(x_log_pricechange_val)
# print(x_log_pricechange)
# y_log_pricechange = [x_log_pricechange.count(i) for i in x_log_pricechange]
# 
# x_pricechange = []
# for i in range(5, 790, 1):
#     x_pricechange_val = kospi_dict['006840']['close'].iloc[i] - kospi_dict['006840']['close'].iloc[i+1]
#     #x_pricechange_val = round(x_log_pricechange_val, 1)
#     x_pricechange.append(x_pricechange_val)
# print(x_pricechange)
# y_pricechange = [x_pricechange.count(i) for i in x_pricechange]
# 
# log_price_dist.bar(x_price, y_price, width = 0.003)
# log_pricechange_dist.bar(x_log_pricechange, y_log_pricechange, width = 0.003)
# pricechange_dist.bar(x_pricechange, y_pricechange, width = 30)
# plt.pyplot.show
# =============================================================================

#code to see the logarithmic price distribution and lograithmic price change distribution
test_list = ['000150', '000815', '000240']
for test_stock in test_list:
    fig = plt.pyplot.figure()
    fig.tight_layout()
    log_price_dist = fig.add_subplot(3, 1, 1)
    log_pricechange_dist = fig.add_subplot(3, 1, 2)
    pricechange_dist = fig.add_subplot(3, 1, 3)
    
    x_price = []
    for i in range(5, 790, 1):
        x_price_val = np.log(kospi_dict[test_stock]['close'].iloc[i])
        x_price_val = round(x_price_val, 2)
        x_price.append(x_price_val)   
    print(x_price)    
    y_price = [x_price.count(i) for i in x_price]
    print(y_price)
    
    x_log_pricechange = []
    for i in range(5, 790, 1):
        x_log_pricechange_val = np.log((kospi_dict[test_stock]['close'].iloc[i])/kospi_dict[test_stock]['close'].iloc[i+1])
        x_log_pricechange_val = round(x_log_pricechange_val, 3)
        x_log_pricechange.append(x_log_pricechange_val)
    print(x_log_pricechange)
    y_log_pricechange = [x_log_pricechange.count(i) for i in x_log_pricechange]
    
    x_pricechange = []
    for i in range(5, 790, 1):
        x_pricechange_val = kospi_dict[test_stock]['close'].iloc[i] - kospi_dict[test_stock]['close'].iloc[i+1]
        #x_pricechange_val = round(x_log_pricechange_val, 1)
        x_pricechange.append(x_pricechange_val)
    print(x_pricechange)
    y_pricechange = [x_pricechange.count(i) for i in x_pricechange]
    
    log_price_dist.bar(x_price, y_price, width = 0.003)
    log_price_dist.set_xlabel('log(price)')
    log_price_dist.set_ylabel('counts(N)')
    
    log_pricechange_dist.bar(x_log_pricechange, y_log_pricechange, width = 0.003)
    log_pricechange_dist.set_xlabel('log(price(t)/price(t+1))')
    log_pricechange_dist.set_ylabel('counts(N)')
    
    pricechange_dist.bar(x_pricechange, y_pricechange, width = 30)
    pricechange_dist.set_xlabel('price(t)/price(t+1)')
    pricechange_dist.set_ylabel('counts(N)')
    plt.pyplot.show
