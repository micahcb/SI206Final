#x axis: cities
#y axis: average rating stars per city
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
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
        dic['city'] = restaurant[4]
        ls.append(dic)
    return all_of

def make_graph(tup):
    mia_ls = []
    bou_ls = []
    for i in tup:
        if i[4] == 1:
            bou_ls.append(i[3])
        else:
            mia_ls.append(i[3])
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

    plt.bar(x, y, color = 'blue')
    plt.xlabel("City Name")
    plt.ylabel("Average Bar Rating")
    plt.title("Average Bar Ratings for Boulder,CO and Miami, FL")

d = get_restaurant_data('yelpXcovid.db')
make_graph(d)
    