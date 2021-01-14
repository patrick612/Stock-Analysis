# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 16:14:11 2021

@author: Runner
"""


import pandas as pd
import sqlite3

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
