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


results_y = sorted(categories_yelp.items(), key = lambda t:t[1], reverse = True)
print(results_y)

#ZOMATO
cur.execute("SELECT category FROM Zomato")
categories_zomato = dict()
for row in cur:
    cat = row[0]
    categories_zomato[cat] = categories_zomato.get(cat, 0) + 1


results_z = sorted(categories_zomato.items(), key = lambda t:t[1], reverse = True)
print(results_z)

#Ave Star Rating by Category

#YELP

print('------------Average Star Rating by Category------------')

print('--------YELP----------')


cur.execute("SELECT category, rating FROM Yelp")
rating_by_cat_y = {}
for row in cur:
    cat = row[0]
    rating = row[1]
    if cat in rating_by_cat_y:
        rating_by_cat_y[cat].append(rating)
    else:
        rating_by_cat_y[cat] = [rating]

print (rating_by_cat_y)

for cat in rating_by_cat_y:
    avg = sum(rating_by_cat_y[cat])/len(rating_by_cat_y[cat])
    rounded = round(avg, 2)
    print(cat + ': ' + str(rounded))
  


#ZOMATO

print('--------ZOMATO----------')

cur.execute("SELECT category, rating FROM Zomato")
rating_by_cat_z = {}
for row in cur:
    cat = row[0]
    rating = row[1]
    if cat in rating_by_cat_z:
        rating_by_cat_z[cat].append(rating)
    else:
        rating_by_cat_z[cat] = [rating]



for cat in rating_by_cat_z:
    avg = sum(rating_by_cat_z[cat])/len(rating_by_cat_z[cat])
    rounded = round(avg, 2)
    print(cat + ': ' + str(rounded))
  
    
#average star rating based on price range
#YELP
cur.execute("SELECT rating, price FROM Yelp")
rating_by_price_y = dict()
for row in cur:
    rating = row[0]
    price = row[1]
    if price in rating_by_price_y:
        rating_by_price_y[price].append(rating)
    else:
        rating_by_price_y[price] = [rating]

rating_by_price_averages_y = dict()
for price in rating_by_price_y:
    ratings = rating_by_price_y[price]
    avg = sum(ratings)/len(ratings)
    rating_by_price_averages_y[price] = round(avg, 2)

print("Yelp")
print(sorted(rating_by_price_averages_y.items(), key = lambda t:t[1], reverse = True))

#ZOMATO
cur.execute("SELECT rating, price FROM Zomato")
rating_by_price_z = dict()
for row in cur:
    rating = row[0]
    price = row[1]
    if price in rating_by_price_z:
        rating_by_price_z[price].append(rating)
    else:
        rating_by_price_z[price] = [rating]

rating_by_price_averages_z = dict()
for price in rating_by_price_z:
    ratings = rating_by_price_z[price]
    avg = sum(ratings)/len(ratings)
    rating_by_price_averages_z[price] = round(avg, 2)

print("Zomato")
print(sorted(rating_by_price_averages_z.items(), key = lambda t:t[1], reverse = True))

#overall average star rating for all restaurants
#YELP
cur.execute("SELECT rating FROM Yelp")
ratings_yelp = list()
for row in cur:
    ratings_yelp.append(row[0])
avg_rating_yelp = round(sum(ratings_yelp)/len(ratings_yelp),4)
print("Yelp Overall Average Star Rating")
print(avg_rating_yelp)

#ZOMATO
cur.execute("SELECT rating FROM Zomato")
ratings_zomato = list()
for row in cur:
    ratings_zomato.append(row[0])
avg_rating_zomato = round(sum(ratings_zomato)/len(ratings_zomato),4)
print("Zomato Overall Average Star Rating")
print(avg_rating_zomato)
