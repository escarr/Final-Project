# analysis
import sqlite3
conn = sqlite3.connect('rest_data.sqlite')
cur = conn.cursor()

#number of restaurants in each category
cur.execute("SELECT category FROM Yelp")
count = 0
for row in cur:
    print(row[0])
    count = count + 1
print(count)