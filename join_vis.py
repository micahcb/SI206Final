#join where state_id and city_id are the same.
#average price on one bar and average covid danger on another
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import csv

def get_pop_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    ls = []
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT * FROM covid_data JOIN Yelp_Data ON covid_data.state_id = Yelp_Data.city_id WHERE covid_data.county = 'Boulder County'")
    all_of = cur.fetchall()
    for rest in all_of:
        dic = {}
        dic['name'] = rest[7]
        dic['covid_impact'] = rest[5]
        dic['num_reviews'] = rest[10]
        ls.append(dic)
    return ls

def make_graph(dic):
    restaurant_ls = []
    impact_ls = []
    for res in dic:
        restaurant_ls.append(res['name'])
        impact_ls.append((res['num_reviews']) / (res['covid_impact']))
    #make new dict to write to file with
    dic2 = []
    for re in dic:
        rest_dic = {}
        rest_dic['name'] = re['name']
        rest_dic['covid_impact'] = (re['num_reviews']) / (re['covid_impact'])
        dic2.append(rest_dic)
    with open('join_vis.csv', 'w', newline='', ) as csvfile:
        fieldnames = ['name', 'covid_impact']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rest in dic2:
            writer.writerow(rest)
    return restaurant_ls, impact_ls


d = get_pop_data('yelpXcovid.db')
x,y = make_graph(d)
plt.barh(x, y, color = 'green')
plt.xlabel("Covid Impact (numreviews/covid_impact)")
plt.ylabel("Bar Name")
plt.title("Covid Effect On Reviews of Bars in Boulder, CO")
plt.show()
    