# FINAL PROJECT
# Rachel Becker, Rachel Lawlor, Alana Woloshin

import requests
import sqlite3
import spotifyinfo, yelpinfo, skyscanner



def get_data(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Restaurants (name TEXT, rating DECIMAL, reviews INTEGER, country TEXT')
    cur.execute('SELECT * FROM Restaurants')
    data = cur.fetchall()

    params_dict = {'Authorization': 'Bearer' + yelpinfo.api}
    r1 = requests.get('https://api.yelp.com/v3/businesses/search?location=Amsterdam&categories=dinner&limit=20', params = params_dict)
    for x in r1.json()['businesses']:
      rating = x['rating']
      restaurant_name= x['name']
      reviews= x['review_count']
      city= x['location']['city']
      cur.execute('INSERT INTO Restaurants (restaurant_name, rating, reviews, city) VALUES (?, ?, ?, ?)', (restaurant_name, rating, reviews, city))
    conn.commit()

    r2 = requests.post("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/v1.0",headers={
    "X-RapidAPI-Host": skyscanner.apihost, "X-RapidAPI-Key": skyscanner.apikey, "Content-Type": "application/x-www-form-urlencoded"}, params ={
    "inboundDate": "2019-06-10",
    "cabinClass": "business",
    "children": 0,
    "infants": 0,
    "country": "US",
    "currency": "USD",
    "locale": "en-US",
    "originPlace": "DTW-sky",
    "destinationPlace": "AMS-sky",
    "outboundDate": "2019-07-01",
    "adults": 3
  })