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
    cur.execute("SELECT * FROM covid_Data")
    all_of = cur.fetchall()
    for county in all_of:
        dic = {}
        dic['population'] = county[3]
        dic['county'] = county[2]
        ls.append(dic)
    return ls

def make_graph(dic):
    pop_ls = []
    county_ls = []
    for county in dic:
        pop_ls.append(county['population'])
        county_ls.append(county['county'])
    with open('county_pop.csv', 'w', newline='', ) as csvfile:
        fieldnames = ['county', 'population']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for county_num in dic:
            writer.writerow(county_num)
    return county_ls, pop_ls


d = get_pop_data('yelpXcovid.db')
x,y = make_graph(d)
plt.barh(x, y, color = 'green')
plt.xlabel("Population")
plt.ylabel("County")
plt.title("Population of Counties in Florida and Colorado")
plt.show()
    