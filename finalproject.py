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
    r1 = requests.get('https://api.yelp.com/v3/businesses/search?location=Amsterdam&categories=dinner&limit=25', params = params_dict)
    r2 = requests.get("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/v1.0",headers={
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