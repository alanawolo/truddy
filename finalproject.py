# FINAL PROJECT
# Rachel Becker, Rachel Lawlor, Alana Woloshin

import requests
import sqlite3
import itunesinfo, yelpinfo
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
  cur.execute('CREATE TABLE IF NOT EXISTS Events (name TEXT, priceMin Integer UNIQUE, priceMax Integer)')
  cur.execute('SELECT * FROM Events')
  data = cur.fetchall()
  r2 = requests.get("https://app.ticketmaster.com/discovery/v2/events?apikey=J0BKwKyQOuE9li4P2HDD1J4Ho2JWug95&size=20&countryCode=NL")
  for x in r2.json()['_embedded']['events']:
    name = x['name']
    priceMin = x['priceRanges'][1]['min']
    priceMax = x['priceRanges'][1]['max']
    cur.execute('INSERT OR IGNORE INTO Events (name, priceMin, priceMax) VALUES (?, ?, ?)', (name, priceMin, priceMax))
  conn.commit()

  # Playlist Data
  cur.execute('CREATE TABLE IF NOT EXISTS Playlist (artistName TEXT, trackName TEXT, trackTimeMillis INT UNIQUE)')
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
  return 'Database Created' 
  
  
# # CALCULATIONS
def calulations(database):
# # Restaurants
# average rating of a Restaurant in Amsterdam = ?
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute('SELECT rating FROM Restaurants')
  total = 0
  count = 0
  for rate in cur:
    total += rate[0]
    count += 1
  average_restaurant_rating = (total/count)
  print(average_restaurant_rating)

# Events
# Average maximum price
  cur.execute('SELECT priceMax FROM Events')
  total = 0
  count = 0
  for price in cur:
    total += price[0]
    count += 1
  average_max_price = (total/count)
  print(average_max_price)

# Average minimum price
  cur.execute('SELECT priceMin FROM Events')
  total = 0
  count = 0
  for price2 in cur:
    total += price2[0]
    count += 1
  average_min_price = (total/count)
  print(average_min_price)

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
  return 'Calculations Done'


# PLOTS!!!!!!!
def plots(database):
# Restaurants plot ... plotting the ratings of the restaurants
  conn = sqlite3.connect(database)
  cur = conn.cursor()
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

  plt.bar(name_list[0:5], ratings_list[0:5], align='center', color = ['magenta', 'indigo', 'blue', 'teal', 'aquamarine'])
  plt.ylabel('Rating')
  plt.xlabel('Restaurant Name')
  plt.title('Ratings of Amsterdam Restaurants')
  plt.xticks(rotation=30)
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

  plt.bar(song_list[0:5], times_list[0:5], align='center', color = ['magenta', 'indigo', 'blue', 'teal', 'aquamarine'])
  plt.ylabel('Time')
  plt.xlabel('Song Name')
  plt.title('Length of Songs')
  plt.xticks(rotation=30)
  plt.savefig('Playlist_Plot.png')
  plt.show() 

# Events plot ... plotting the min price for top 5 events
  cur.execute('SELECT name FROM Events')
  name_list = []
  for name in cur:
    name_list.append(name[0])

  cur.execute('SELECT priceMin FROM Events')
  min_list = []
  for min_price in cur:
    min_list.append(min_price[0])
  plt.bar(name_list[0:5], min_list[0:5], align='center', color = ['lime', 'blueviolet', 'lavender', 'plum'])
  plt.ylabel('Minimum Price')
  plt.xlabel('Event Name')
  plt.title('Minimum Prices of Events')
  plt.xticks(rotation=20)
  plt.savefig('Prices_event.png')
  plt.show() 
  
# Events plot ... plotting the max price vs min prive
  cur.execute('SELECT priceMax FROM Events')
  max_list = []
  for max_price in cur:
    max_list.append(max_price[0])
  plt.scatter(min_list,max_list)
  plt.xlabel('Minimim Price')
  plt.ylabel('Maximum Price')
  plt.title('Minimum vs Maximum Prices of Events in Amsterdam')
  plt.savefig('Event_plot.png')
  plt.show()

  return 'Plots Made'

print(get_data('final_project.sqlite'))
print(calulations('final_project.sqlite'))
print(plots('final_project.sqlite'))