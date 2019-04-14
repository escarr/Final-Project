# analysis
import sqlite3
import json
conn = sqlite3.connect('rest_data.sqlite')
cur = conn.cursor()

#number of restaurants in each category
#YELP
cur.execute("SELECT category FROM Yelp")
categories_yelp = dict()
for row in cur:
    cat = row[0]
    categories_yelp[cat] = categories_yelp.get(cat, 0) + 1


print(sorted(categories_yelp.items(), key = lambda t:t[1], reverse = True))

#ZOMATO
cur.execute("SELECT category FROM Zomato")
categories_zomato = dict()
for row in cur:
    cat = row[0]
    categories_zomato[cat] = categories_zomato.get(cat, 0) + 1


print(sorted(categories_zomato.items(), key = lambda t:t[1], reverse = True))
