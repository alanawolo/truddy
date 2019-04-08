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
