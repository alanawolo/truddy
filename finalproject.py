# FINAL PROJECT
# Rachel Becker, Rachel Lawlor, Alana Woloshin

import requests
import sqlite3
import spotifyinfo, yelpinfo, weather


def get_data(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Restaurants (name TEXT PRIMARY KEY, rating DECIMAL, reviews INTEGER, country TEXT)')
    cur.execute('SELECT * FROM Restaurants')
    data = cur.fetchall()

    params_dict = {'Authorization':'Bearer ' + yelpinfo.api}
    r1 = requests.get('https://api.yelp.com/v3/businesses/search?location=Amsterdam&categories=dinner&limit=20', headers = params_dict)

    for x in r1.json()['businesses']:
      rating = x['rating']
      restaurant_name= x['name']
      reviews= x['review_count']
      city= x['location']['city']
      cur.execute('INSERT OR IGNORE INTO Restaurants (name, rating, reviews, country) VALUES (?, ?, ?, ?)', (restaurant_name, rating, reviews, city))
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS Weather (temp INTEGER, humidity INTEGER, mintemp INTEGER, maxtemp INTEGER)')
    cur.execute('SELECT * FROM Weather')
    data = cur.fetchall()
    
    #this ket should be updated in a couple hours
    r2 = requests.get('https://api.openweathermap.org/data/2.5/weather/?q=Amsterdam&cnt=20&APPID=318f31fd15810fe42b21f896c93c2779')
    for x in r2.json().items():
      if x[0] == 'main':
        temp = x[1]['temp']
        hum= x[1]['humidity']
        mintemp = x[1]['temp_min']
        maxtemp = x[1]['temp_max']
        cur.execute('INSERT INTO Weather (temp, humidity, mintemp,maxtemp) VALUES (?, ?, ?, ?)', (temp,hum, mintemp,maxtemp))
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS Playlist (artistName TEXT, trackName TEXT, trackTimeMillis INT)')
    cur.execute('SELECT * FROM Playlist')
    data = cur.fetchall()

    params_dict = {'term': 'Amsterdam', 'country': "US", 'media': 'music'}
    r3 = requests.get('https://itunes.apple.com/search?', params = params_dict)
    print(r3.json())
    for x in r3.json()['results']:
      artistName = x['artistName']
      trackName= x['trackName']
      trackTimeMillis = x['trackTimeMillis']
      cur.execute('INSERT OR IGNORE INTO Playlist (artistName, trackName, trackTimeMillis) VALUES (?, ?, ?)', (artistName, trackName, trackTimeMillis))
    conn.commit()
    cur.execute('SELECT * FROM Playlist')
    data = cur.fetchall()

    db_data = cur.execute('SELECT * FROM Restaurants, Weather, Playlist')
    return 'Database created'
print(get_data('final_project.sqlite'))
