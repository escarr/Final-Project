#load required libraries
import requests
import json
import sqlite3

#YELP 
api_key = "iY64_sEJScpK8aXweuNaBZB7OsM6_DEeWY6LxAgugsrpMXSDX0sgAh6_IWHcs6b0oN-zfrjKgJ8JxFSGLsBYkhZeOEcRH-eoW9Y__dygbykb5ybTl8caYcyuKlWiXHYx"
headers = {"Authorization": "Bearer %s" % api_key}
client_id = "eTc8qMaxcsJi1x6b3YqrFw"

url = "https://api.yelp.com/v3/businesses/search"

#offsets so we can get 100 restaurants for each city
offsets = (0, 20, 40, 60, 80)

#create database
conn = sqlite3.connect('rest_data.sqlite')
cur = conn.cursor()

#ask user for city
user_input= input("Please Enter a City:")

cur.execute("CREATE TABLE IF NOT EXISTS YELP(name TEXT, city TEXT, rating INTEGER, price TEXT, category TEXT, num_reviews INTEGER, id TEXT PRIMARY KEY)")

for offset in offsets:
    params = {"location": user_input, "offset": offset}

    req = requests.get(url, params = params, headers = headers)

    rests = json.loads(req.text)

    for rest in rests["businesses"]:
        sql = "INSERT OR IGNORE INTO Yelp (name, city, rating, price, category, num_reviews, id) VALUES (?, ?, ?, ?, ?, ?, ?)"
        categories = list()
        for cat in rest["categories"]:
            categories.append(cat["title"])
        val = (rest["name"], rest["location"]["city"], rest["rating"], rest.get("price", 'NA'), categories[0], rest["review_count"], rest["id"])
        cur.execute(sql, val)

#ZOMATO
api_key = "dac0fbe3854024b18110f1217f9c32df"
url = "https://developers.zomato.com/api/v2.1/search"
headers = {"user-key" : api_key}
offsets = (0, 20, 40, 60, 80)

cur.execute("CREATE TABLE IF NOT EXISTS Zomato(name TEXT, city TEXT, rating INTEGER, price TEXT, category TEXT, num_reviews INTEGER, id TEXT PRIMARY KEY)")

city_name = user_input.split(' ')
city_name = '%20'.join(city_name)

#getting location ID
url = "https://developers.zomato.com/api/v2.1/locations?query=" + city_name
req = requests.get(url, headers = headers)
location_text = json.loads(req.text)
city_id = location_text["location_suggestions"][0]["city_id"]


url = "https://developers.zomato.com/api/v2.1/search"

for offset in offsets:
        
    params = {"start": offset, "count": 20, "entity_id" : city_id, "entity_type" : "city", "q" : user_input}

    req = requests.get(url, headers = headers, params= params)

    rest_text = json.loads(req.text)

    for rest in rest_text["restaurants"]:
        rest = rest["restaurant"]
        sql = "INSERT OR IGNORE INTO Zomato (name, city, rating, price, category, num_reviews, id) VALUES (?, ?, ?, ?, ?, ?, ?)"
        categories = rest["cuisines"].split(",")
        val = (rest["name"], rest["location"]["locality"], rest["user_rating"]["aggregate_rating"], rest.get("price_range", 'NA'), categories[0], rest["user_rating"]["votes"], rest["R"]["res_id"])
        cur.execute(sql, val)
        
conn.commit()