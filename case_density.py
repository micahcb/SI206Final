import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import csv

def get_restaurant_data(db_filename):
    ls = []
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT * FROM covid_Data")
    all_of = cur.fetchall()
    for county in all_of:
        dic = {}
        dic['state'] = county[1]
        dic['county'] = county[2]
        dic['population'] = county[3]
        dic['case_density'] = county[4]
        ls.append(dic)
    return ls

def make_graph(dic):
    fl_ls = []
    co_ls = []
    for i in dic:
        if i['state'] == 1:
            co_ls.append(i['case_density'])
        else:
            fl_ls.append(i['case_density'])
    fl_tot = len(fl_ls)
    co_tot = len(co_ls)
    fl_ave = 0
    co_ave = 0
    for i in co_ls:
        co_ave += i
    for i in fl_ls:
        fl_ave += i
    fl_ave = fl_ave / fl_tot
    co_ave = co_ave / co_tot
    x = ['Colorado', 'Florida']
    y = [co_ave, fl_ave]
    with open('case_density.csv', 'w', newline='', ) as csvfile:
        fieldnames = ['state', 'county', 'population', 'case_density']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for county_num in dic:
            writer.writerow(county_num)
    return x,y


d = get_restaurant_data('yelpXcovid.db')
x,y = make_graph(d)
plt.bar(x, y, color = 'tomato')
plt.xlabel("State Name")
plt.ylabel("Average Case Density Per County")
plt.title("Average Case Density Per County For Florida and Colorado")
plt.show()
    