#load required libraries
import requests
import json
import sqlite3

def main():
    #create database connection
    conn = sqlite3.connect('rest_data.sqlite')
    cur = conn.cursor()

    #YELP 
    api_key = ''
    headers = {"Authorization": "Bearer %s" % api_key}
    url = "https://api.yelp.com/v3/businesses/search"

    cur.execute("CREATE TABLE IF NOT EXISTS YELP(name TEXT, city TEXT, rating INTEGER, price TEXT, category TEXT, num_reviews INTEGER, id TEXT PRIMARY KEY)")

    #get current count of number of restaurants in database to know where to start
    cur.execute("SELECT id FROM Yelp")
    count = 0
    for row in cur:
        count = count + 1
    print(count)

    params = {"location": "Ann Arbor", "offset": count}
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
    api_key = ''
    url = "https://developers.zomato.com/api/v2.1/search?entity_id=285&entity_type=city&q=Ann%20Arbor"
    headers = {"user-key" : api_key}

    cur.execute("CREATE TABLE IF NOT EXISTS Zomato(name TEXT, city TEXT, rating INTEGER, price TEXT, category TEXT, num_reviews INTEGER, id TEXT PRIMARY KEY)")

    #get current count of number of restaurants in database to know where to start
    cur.execute("SELECT id FROM Zomato")
    count = 0
    for row in cur:
        count = count + 1
    print(count)

    params = {"start": count, "count": 20}
    req = requests.get(url, headers = headers, params= params)
    rest_text = json.loads(req.text)

    for rest in rest_text["restaurants"]:
        rest = rest["restaurant"]
        sql = "INSERT OR IGNORE INTO Zomato (name, city, rating, price, category, num_reviews, id) VALUES (?, ?, ?, ?, ?, ?, ?)"
        categories = rest["cuisines"].split(",")
        val = (rest["name"], rest["location"]["locality"], rest["user_rating"]["aggregate_rating"], rest.get("price_range", 'NA'), categories[0], rest["user_rating"]["votes"], rest["R"]["res_id"])
        cur.execute(sql, val)
        
    conn.commit()

#call function
if __name__ == "__main__":
    main()
