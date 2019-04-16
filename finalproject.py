# FINAL PROJECT
# Rachel Becker, Rachel Lawlor, Alana Woloshin

import requests
import sqlite3
import spotifyinfo, yelpinfo
import matplotlib.pyplot as plt


def get_data(database):
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  # Restaurant Data
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

  # Event Data
  cur.execute('CREATE TABLE IF NOT EXISTS Events (name TEXT, priceMin Integer, priceMax Integer)')
  cur.execute('SELECT * FROM Events')
  data = cur.fetchall()
  r2 = requests.get("https://app.ticketmaster.com/discovery/v2/events?apikey=J0BKwKyQOuE9li4P2HDD1J4Ho2JWug95&size=20&countryCode=NL")
  for x in r2.json()['_embedded']['events']:
    print(x)
    name = x['name']
    print(name)
    priceMin = x['priceRanges'][1]['min']
    print(priceMin)
    priceMax = x['priceRanges'][1]['max']
    print(priceMax)
    cur.execute('INSERT INTO Events (name, priceMin, priceMax) VALUES (?, ?, ?)', (name, priceMin, priceMax))
  conn.commit()

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
  
  
  
# # CALCULATIONS

# # Restaurants
# average rating of a Restaurant in Amsterdam = ?
  cur.execute('SELECT rating FROM Restaurants')
  total = 0
  count = 0
  for rate in cur:
    total += rate[0]
    count += 1
  average_restaurant_rating = (total/count)
  print(average_restaurant_rating)


# Playlist
# average song length
  cur.execute('SELECT trackTimeMillis FROM Playlist')
  total = 0
  count = 0
  for time in cur:
    time_in_seconds = time[0] * (0.001/1)
    total += time_in_seconds
    count += 1
  average_song_length_in_seconds = (total/count)
  print(average_song_length_in_seconds)



# PLOTS!!!!!!!

# Restaurants plot ... plotting the ratings of the restaurants
  cur.execute('SELECT name FROM Restaurants')
  name_list = []
  for name in cur:
    name_list.append(name[0])

  cur.execute('SELECT rating FROM Restaurants')
  ratings_list = []
  for rate in cur:
    ratings_list.append(rate[0])

  data = {}
  count = 0
  for x in name_list:
    if x not in data:
      data[x] = ratings_list[count]
    count += 1 

  plt.bar(name_list[0:5], ratings_list[0:5], align='center', color = ['magenta', 'red', 'indigo', 'blue', 'orange', 'pink', 'purple', 'violet', 'green', 'black', 'gray', 'yellow', 'navy', 'teal', 'aquamarine', 'cyan', 'lime', 'blueviolet', 'lavender', 'plum'])
  plt.ylabel('Rating')
  plt.xlabel('Restaurant Name')
  plt.title('Ratings of Amsterdam Restaurants')
  plt.savefig('Restaurant_Plot.png')
  plt.show()  

  # Playlist plot ... plotting the length of songs
  cur.execute('SELECT trackName FROM Playlist')
  song_list = []
  for song in cur:
    song_list.append(song[0])

  cur.execute('SELECT trackTimeMillis FROM Playlist')
  times_list = []
  for time in cur:
    time_in_seconds = time[0] * (0.001/1)
    times_list.append(time_in_seconds)

  data = {}
  count2 = 0
  for x in song_list:
    if x not in data:
      data[x] = times_list[count2]
    count2 += 1 

  plt.bar(song_list[0:5], times_list[0:5], align='center', color = ['magenta', 'red', 'indigo', 'blue', 'orange', 'pink', 'purple', 'violet', 'green', 'black', 'gray', 'yellow', 'navy', 'teal', 'aquamarine', 'cyan', 'lime', 'blueviolet', 'lavender', 'plum'])
  plt.ylabel('Time')
  plt.xlabel('Song Name')
  plt.title('Length of Songs')
  plt.savefig('Playlist_Plot.png')
  plt.show() 

  return 'Database Created'
print(get_data('final_project.sqlite'))

