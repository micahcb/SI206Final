import json
from xxlimited import new 
import requests 
import sqlite3
import os
api_key = 'dL9sPP12tM--3gqK0Z7MZ-gIaRf88oj0HrdIcrxgO7t0P1ncXJ4j99dm5NlriAbPu4viW7JuoKYTgan_YZGQtWIKMdyliReErXouox1jfB2E5QTI2mX-POulcpdUYnYx'

def yelp_data(api_key, city, cur, conn):
    b_url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization" : "Bearer %s" % api_key}
    cur.execute("SELECT MAX (id) from Yelp_Data")
    x = cur.fetchone()[0] + 24
    params = {'term': 'bar', 'location': city, 'sort_by': 'rating', 'limit': x,}
    request = requests.get(b_url, headers = headers, params = params)
    response = json.loads(request.text)
    response = response["businesses"][x-25:]
    print(response)
    dat = []
    for item in response['businesses']:
        if item['id'] not in dat and 'price' in item.keys():
            dat.append((item['name'], item['price'], item['rating'], item['location']['city']))
    return dat


def fill_database(data, cur, conn):
    try:
        for tup in data:
            cur.execute("INSERT OR IGNORE INTO Yelp_Data (restaurant_name, price_range, rating, city) VALUES (?,?,?,?)", (tup[0], tup[1], tup[2], tup[3]))
            conn.commit()
        print("Successfully added")
    except:
        print('ERROR')

def new_database(): 
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ 'yelpxespn.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Yelp_Data (id INTEGER PRIMARY KEY, restaurant_name TEXT, price_range TEXT, rating FLOAT, city TEXT)")
    conn.commit()
    return cur, conn

cur, conn = new_database()
fill_database(yelp_data(api_key, 'Boulder'), cur, conn)
fill_database(yelp_data(api_key, 'Miami'), cur, conn)