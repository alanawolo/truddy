# FINAL PROJECT
# Rachel Becker, Rachel Lawlor, Alana Woloshin

import requests
import sqlite3
import spotifyinfo, yelpinfo, weather


def get_data(database):
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  # Restaurant Data
  cur.execute('CREATE TABLE IF NOT EXISTS Restaurants (name TEXT PRIMARY KEY, rating DECIMAL, reviews INTEGER, country TEXT)')
  cur.execute('SELECT * FROM Restaurants')
  data = cur.fetchall()
  params_dict = {'Authorization':'Bearer ' + yelpinfo.api}
  r1 = requests.get('https://api.yelp.com/v3/businesses/search?location=Amsterdam&categories=dinner&limit=20', headers = params_dict)
  print(len(r1.json()['businesses']))
  for x in r1.json()['businesses']:
    rating = x['rating']
    restaurant_name= x['name']
    reviews= x['review_count']
    city= x['location']['city']
    cur.execute('INSERT OR IGNORE INTO Restaurants (name, rating, reviews, country) VALUES (?, ?, ?, ?)', (restaurant_name, rating, reviews, city))
  conn.commit()

  # Weather Data
  # cur.execute('CREATE TABLE IF NOT EXISTS Weather (temp INT, humidity INT, mintemp INT, maxtemp INT)')
  # cur.execute('SELECT * FROM Weather')
  # data = cur.fetchall()
  # r2 = requests.get('https://api.openweathermap.org/data/2.5/weather/?q=Amsterdam&cnt=20&APPID=318f31fd15810fe42b21f896c93c2779')
  # print(len(r2.json().items()))
  # for x in r2.json().items():
  #   if x[0] == 'main':
  #     temp = x[1]['temp']
  #     humidity = x[1]['humidity']
  #     mintemp = x[1]['temp_min']
  #     maxtemp = x[1]['temp_max']
  #     cur.execute('INSERT INTO Weather (temp, humidity, mintemp, maxtemp) VALUES (?, ?, ?, ?)', (temp, humidity, mintemp, maxtemp))
  # conn.commit()

  # StubHub Data
  # cur.execute('CREATE TABLE IF NOT EXISTS Events (name TEXT, venue OBJECT, minPrice STRING)')
  # cur.execute('SELECT * FROM Events')
  # data = cur.fetchall()
  # params_dict = {'city': 'Amsterdam', 'country': 'Netherlands', 'sort': 'minPrice', 'rows': 20}
  # r2 = requests.get('https://api.stubhub.com/sellers/search/events/v3', params = params_dict)
  # print(len(r2.json()))
  # print(r2.json())
  # for x in r2.json():
  #   name = x['']
  #   venue = x['']
  #   minPrice = x['']
  #   cur.execute('INSERT INTO Events (name, venue, minPrice) VALUES (?, ?, ?)', (name, venue, minPrice))
  # conn.commit()

  # Playlist Data
  cur.execute('CREATE TABLE IF NOT EXISTS Playlist (artistName TEXT, trackName TEXT, trackTimeMillis INT)')
  cur.execute('SELECT * FROM Playlist')
  data = cur.fetchall()
  params_dict = {'term': 'travel', 'country': 'US', 'media': 'music'}
  r3 = requests.get('https://itunes.apple.com/search?limit=20', params = params_dict)
  for item in r3.json()['results']:
    artistName = item['artistName']
    trackName= item['trackName']        
    trackTimeMillis = item['trackTimeMillis']
    cur.execute('INSERT OR IGNORE INTO Playlist (artistName, trackName, trackTimeMillis) VALUES (?, ?, ?)', (artistName, trackName, trackTimeMillis))
  conn.commit()
  
  db_data = cur.execute('SELECT * FROM Restaurants, Playlist')
  return 'Database created'

print(get_data('final_project.sqlite'))

# calculations
# for Restaurants ... average rating of a Restaurant in Amsterdam = ?
# for Playlist ... average song length
