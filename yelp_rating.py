#x axis: cities
#y axis: average rating stars per city
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
    cur.execute("SELECT * FROM Yelp_Data")
    all_of = cur.fetchall()
    for restaurant in all_of:
        dic = {}
        dic['name'] = restaurant[1]
        dic['rating'] = restaurant[3]
        dic['city'] = restaurant[5]
        ls.append(dic)
    return ls

def make_graph(dic):
    mia_ls = []
    bou_ls = []
    for i in dic:
        if i['city'] == 1:
            bou_ls.append(i['rating'])
        else:
            mia_ls.append(i['rating'])
    mia_tot = len(mia_ls)
    bou_tot = len(bou_ls)
    mia_ave = 0
    bou_ave = 0
    for i in bou_ls:
        bou_ave += i
    for i in mia_ls:
        mia_ave += i
    mia_ave = mia_ave / mia_tot
    bou_ave = bou_ave / bou_tot
    x = ['Boulder', 'Miami']
    y = [bou_ave, mia_ave]
    with open('yelp_rating.csv', 'w', newline='', ) as csvfile:
        fieldnames = ['name', 'rating', 'city']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for county_num in dic:
            writer.writerow(county_num)
    return x,y


d = get_restaurant_data('yelpXcovid.db')
x,y = make_graph(d)
plt.bar(x, y, color = 'orange')
plt.xlabel("City Name")
plt.ylabel("Average Bar Rating")
plt.title("Average Bar Ratings for Boulder,CO and Miami, FL")
plt.show()
    