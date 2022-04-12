import json
import requests 
import sqlite3
import os
def covid_data(state):
    b_url = "https://api.covidactnow.org/v2/county/{}.json?apiKey=9c5489f3141b4afc87a835087e5e33d2"
    formatted_url = b_url.format(state)
    request = requests.get(formatted_url)
    response = json.loads(request.text)
    dat = []
    for item in response:
        dat.append((state, item['county'], item['population'], item['metrics']['caseDensity'], item['riskLevels']['overall']))
    return dat


def fill_database(data, cur, conn, cur2, conn2):
    try:
        for tup in data:
            cur.execute("SELECT id FROM covid_state_data WHERE state = ?", (tup[0],))
            x = cur.fetchone()[0]
            cur2.execute("INSERT OR IGNORE INTO covid_Data (state_id, county, population, caseDensity, riskLevel) VALUES (?,?,?,?,?)", (x, tup[1], tup[2], tup[3], tup[4]))
            conn.commit()
            conn2.commit()
        print("Successfully added")
    except:
        print('ERROR')

def new_database(): 
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ 'yelpxespn.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS covid_Data (id INTEGER PRIMARY KEY, state_id INTEGER, county TEXT, population INTEGER, caseDensity FLOAT, riskLevel INTEGER)")
    conn.commit()
    return cur, conn
def covid_state_database():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ 'yelpxespn.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS covid_state_data (id INTEGER PRIMARY KEY, state TEXT)")
    cur.execute("INSERT OR IGNORE INTO covid_state_data VALUES(?,?)",(1,'CO'))
    cur.execute("INSERT OR IGNORE INTO covid_state_data VALUES(?,?)",(1, 'FL'))
    conn.commit()
    return cur, conn

state_cur, state_conn = covid_state_database()
data_cur, data_conn = new_database()
fill_database(covid_data('CO')[:25], state_cur, state_conn, data_cur, data_conn)
fill_database(covid_data('FL')[:25], state_cur, state_conn, data_cur, data_conn)
fill_database(covid_data('CO')[25:50], state_cur, state_conn, data_cur, data_conn)
fill_database(covid_data('FL')[25:50], state_cur, state_conn, data_cur, data_conn)




#create dict w state names.
#create table with state names and ids
#match ids with entries into covid_data
#make sure max 25