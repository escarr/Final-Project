
import requests
import json
import sqlite3

#YELP 
api_key = "iY64_sEJScpK8aXweuNaBZB7OsM6_DEeWY6LxAgugsrpMXSDX0sgAh6_IWHcs6b0oN-zfrjKgJ8JxFSGLsBYkhZeOEcRH-eoW9Y__dygbykb5ybTl8caYcyuKlWiXHYx"
headers = {"Authorization": "Bearer %s" % api_key}
client_id = "eTc8qMaxcsJi1x6b3YqrFw"

url = "https://api.yelp.com/v3/businesses/search"

offsets = (0, 20, 40, 60, 80)

conn = sqlite3.connect('rest_data.sqlite')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Yelp")
cur.execute("CREATE TABLE YELP(name TEXT, city TEXT, rating INTEGER, price TEXT, category TEXT, num_reviews INTEGER)")

for offset in offsets:
    params = {"location": "Ann Arbor", "offset": offset}

    req = requests.get(url, params = params, headers = headers)

    rests = json.loads(req.text)

    for rest in rests["businesses"]:
        sql = "INSERT INTO Yelp (name, city, rating, price, category, num_reviews) VALUES (?, ?, ?, ?, ?, ?)"
        categories = list()
        for cat in rest["categories"]:
            categories.append(cat["title"])
        val = (rest["name"], rest["location"]["city"], rest["rating"], rest.get("price", 'NA'), categories[0], rest["review_count"])
        cur.execute(sql, val)

#ZOMATO
api_key = "dac0fbe3854024b18110f1217f9c32df"
url = "https://developers.zomato.com/api/v2.1/search?entity_id=285&entity_type=city&q=Ann%20Arbor"

headers = {"user-key" : api_key}
offsets = (0, 20, 40, 60, 80)

cur.execute("DROP TABLE IF EXISTS Zomato")
cur.execute("CREATE TABLE Zomato(name TEXT, city TEXT, rating INTEGER, price TEXT, category TEXT, num_reviews INTEGER)")

for offset in offsets:

    params = {"locality" : "Ann Arbor", "start": offset, "count": 20}

    req = requests.get(url, headers = headers, params = params)

    rest_text = json.loads(req.text)

    for rest in rest_text["restaurants"]:
        rest = rest["restaurant"]
        sql = "INSERT INTO Zomato (name, city, rating, price, category, num_reviews) VALUES (?, ?, ?, ?, ?, ?)"
        categories = rest["cuisines"].split(",")
        val = (rest["name"], rest["location"]["locality"], rest["user_rating"]["aggregate_rating"], rest.get("price_range", 'NA'), categories[0], rest["user_rating"]["votes"])
        cur.execute(sql, val)
        
conn.commit()