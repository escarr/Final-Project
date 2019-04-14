
import requests
import json
import sqlite3

#YELP EXAMPLE
api_key = "iY64_sEJScpK8aXweuNaBZB7OsM6_DEeWY6LxAgugsrpMXSDX0sgAh6_IWHcs6b0oN-zfrjKgJ8JxFSGLsBYkhZeOEcRH-eoW9Y__dygbykb5ybTl8caYcyuKlWiXHYx"
headers = {"Authorization": "Bearer %s" % api_key}
client_id = "eTc8qMaxcsJi1x6b3YqrFw"

url = "https://api.yelp.com/v3/businesses/search"

offsets = (0, 20, 40, 60, 80)

conn = sqlite3.connect('yelp.sqlite')
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
        
conn.commit()

#data analysis

#number of restaurants in each category
#cur.execute("SELECT category FROM Yelp")
#category_dict = dict()
#for row in cur:
#    category_dict[row] = category_dict.get(row, 0) + 1

#print(category_dict)

#cur.execute("SELECT category, rating FROM Yelp")
#category_rating_dict = dict()
#for row in cur:
#    category = row[0]
#    rating = row[1]
#    category_rating_dict[category] = category_rating_dict[category].append(rating)


#print(category_rating_dict)
