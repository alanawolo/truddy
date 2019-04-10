# FINAL PROJECT
# Rachel Becker, Rachel Lawlor, Alana Woloshin

import requests
import sqlite3
import spotifyinfo, yelpinfo, weather


def get_data(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Restaurants (name TEXT, rating DECIMAL, reviews INTEGER, country TEXT)')
    cur.execute('SELECT * FROM Restaurants')
    data = cur.fetchall()

    params_dict = {'Authorization':'Bearer '+yelpinfo.api}
    r1 = requests.get('https://api.yelp.com/v3/businesses/search?location=Amsterdam&categories=dinner&limit=20', headers = params_dict)

    for x in r1.json()['businesses']:
      rating = x['rating']
      restaurant_name= x['name']
      reviews= x['review_count']
      city= x['location']['city']
      cur.execute('INSERT INTO Restaurants (name, rating, reviews, country) VALUES (?, ?, ?, ?)', (restaurant_name, rating, reviews, city))
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS Weather (main TEXT, description TEXT, temp INTEGER, humidity INTEGER)')
    cur.execute('SELECT * FROM Weather')
    data = cur.fetchall()
    
    #this ket should be updated in a couple hours
    r2 = requests.get('https://api.openweathermap.org/data/2.5/weather/?q=Amsterdam&cnt=20&APPID=318f31fd15810fe42b21f896c93c2779')
    print(r2.json())
    for x in r2.json()['weather']:
      main = x['weather']['main']
      desc= x['weather']['description']
      temp= x['temp']
      hum= x['humidity']
      cur.execute('INSERT INTO Weather (main, description, temp, humidity) VALUES (?, ?, ?, ?)', (main, desc, temp, hum))
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS Playlist (artistName TEXT, trackName TEXT, contentRatingAdvisory TEXT, trackTimeMillis)')
    cur.execute('SELECT * FROM Playlist')
    data = cur.fetchall()

    params_dict = {'term': artistName}
    r3 = requests.get('https://itunes.apple.com/search?', params = params_dict)
    print(r3.json())
    for x in r3.json()['businesses']:
      artistName = x['artistName']
      trackName= x['trackName']
      contentRatingAdvisory= x['contentRatingAdvisory']
      trackTimeMillis = x['trackTimeMillis']
      cur.execute('INSERT INTO PLaylist (artistName, trackName, contentRatingAdvisory, trackTimeMillis) VALUES (?, ?, ?, ?)', (artistName, trackName, contentRatingAdvisory, trackTimeMillis))
    conn.commit()

    db_data = cur.execute('SELECT * FROM Restaurants, Weather,Playlist')
    return 'Database created'
print(get_data('final_project.sqlite'))
