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
  
    

