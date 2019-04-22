#analysis
import sqlite3
import json
import matplotlib
import matplotlib.pyplot as plt

#create database connection
def main():
    #create database connection

    conn = sqlite3.connect('rest_data.sqlite')
    cur = conn.cursor()

    #open json file for writing to
    write_file = open("data_analysis.json", "w")

    #function to get the number of restaurants in each category
    #takes the column of categories as input
    def get_num_of_rests_by_cat(category_data):
        categories = dict()
        for row in cur:
            cat = row[0]
            categories[cat] = categories.get(cat, 0) + 1
        return categories

    #YELP
    categories_yelp = get_num_of_rests_by_cat(cur.execute("SELECT category FROM Yelp"))
    categories_yelp = {"Yelp Restaurant Category Counts" : categories_yelp}

    #ZOMATO
    categories_zomato = get_num_of_rests_by_cat(cur.execute("SELECT category FROM Zomato"))
    categories_zomato = {"Zomato Restaurant Category Counts" : categories_zomato}

    #Average Star Rating by Category
    #takes the category and rating columns from the database as input
    def get_rating_by_cat(data):
        rating_by_cat = {}
        for row in cur:
            cat = row[0]
            rating = row[1]
            if cat in rating_by_cat:
                rating_by_cat[cat].append(rating)
            else:
                rating_by_cat[cat] = [rating]
        averages = {}
        for cat in rating_by_cat:
            avg = round(sum(rating_by_cat[cat])/len(rating_by_cat[cat]),2)
            averages[cat] = avg
        return averages

    #YELP
    rating_by_cat_yelp = get_rating_by_cat(cur.execute("SELECT category, rating FROM Yelp"))
    rating_by_cat_yelp = {"Yelp Average Star Rating by Restaurant Category" : rating_by_cat_yelp}

    #ZOMATO
    rating_by_cat_zomato = get_rating_by_cat(cur.execute("SELECT category, rating FROM Zomato"))
    rating_by_cat_zomato = {"Zomato Average Star Rating by Restaurant Category" : rating_by_cat_zomato}
    
    #Average star rating based on price range
    #takes the star rating and price range columns from the database as input
    def get_rating_by_price(data):
        rating_by_price = dict()
        for row in cur:
            rating = row[0]
            price = row[1]
            if price in rating_by_price:
                rating_by_price[price].append(rating)
            else:
                rating_by_price[price] = [rating]
        averages = {}
        for price in rating_by_price:
            ratings = rating_by_price[price]
            avg = sum(ratings)/len(ratings)
            averages[price] = round(avg, 2)
        return averages
    
    #YELP
    rating_by_price_yelp = get_rating_by_price(cur.execute("SELECT rating, price FROM Yelp"))
    rating_by_price_yelp = {"Yelp Average Star Rating by Price Range" : rating_by_price_yelp}

    #ZOMATO
    rating_by_price_zomato = get_rating_by_price(cur.execute("SELECT rating, price FROM Zomato"))
    rating_by_price_zomato = {"Zomato Average Star Rating by Price Range" : rating_by_price_zomato}

    #Overall average star rating for all restaurants
    def get_overall_average_rating(ratings):
        ratings = list()
        for row in cur:
            ratings.append(row[0])
        avg_rating = round(sum(ratings)/len(ratings),4)
        return avg_rating

    #YELP
    overall_avg_rating_yelp = get_overall_average_rating(cur.execute("SELECT rating FROM Yelp"))
    overall_avg_rating_yelp = {"Yelp Overall Average Star Rating for All Restaurants" : overall_avg_rating_yelp}

    #ZOMATO
    overall_avg_rating_zomato = get_overall_average_rating(cur.execute("SELECT rating FROM Zomato"))
    overall_avg_rating_zomato = {"Zomato Overall Average Star Rating for All Restaurants" : overall_avg_rating_zomato}

    #write to json file
    yelp_data = {"Yelp Data" : (categories_yelp, rating_by_cat_yelp, rating_by_price_yelp, overall_avg_rating_yelp)}
    zomato_data = {"Zomato Data" : (categories_zomato, rating_by_cat_zomato, rating_by_price_zomato, overall_avg_rating_zomato)}

    json.dump((yelp_data, zomato_data), write_file, indent = 4, sort_keys = True)

    write_file.close()


    #VISUALIZATIONS

    #scatterplot of star rating vs number of reviews

    #YELP
    cur.execute("SELECT rating, num_reviews from Yelp")
    ratings = list()
    num_reviews = list()
    for row in cur:
        ratings.append(row[0])
        num_reviews.append(row[1])

    fig = plt.figure()

    ax1 = fig.add_subplot(121)
    ax1.scatter(ratings, num_reviews, color = 'red')
    ax1.set_xlabel("Ratings")
    ax1.set_ylabel("Number of Reviews")
    ax1.set_title("Yelp: Number of Reviews vs Ratings")
    ax1.set_ylim(0, 2000)

    #ZOMATO
    cur.execute("SELECT rating, num_reviews from Zomato")
    ratings = list()
    num_reviews = list()
    for row in cur:
        ratings.append(row[0])
        num_reviews.append(row[1])

    ax2 = fig.add_subplot(122)
    ax2.scatter(ratings, num_reviews, color = 'red')
    ax2.set_xlabel("Ratings")
    ax2.set_ylabel("Number of Reviews")
    ax2.set_title("Zomato: Number of Reviews vs Ratings")
    ax2.set_ylim(0, 2000)

    fig.savefig("ratings_by_reviews.png")
    plt.show()


    #HISTOGRAM DISTRIBUTION OF STAR RATINGS

    #YELP
    cur.execute("SELECT rating from YELP")
    ratings = list()

    for row in cur:
        ratings.append(row[0])

    fig = plt.figure()

    ax1 = fig.add_subplot(121)
    ax1.hist(ratings, color = 'red')
    ax1.set_xlabel("Ratings")

    ax1.set_title("Yelp: Distribution of Star Ratings")
    ax1.set_ylim(0, 55)

    #ZOMATO
    cur.execute("SELECT rating from Zomato")
    ratings = list()

    for row in cur:
        ratings.append(row[0])


    ax2 = fig.add_subplot(122)
    ax2.hist(ratings, color = 'red')
    ax2.set_xlabel("Ratings")

    ax2.set_title("Zomato: Distribution of Star Ratings")
    ax2.set_ylim(0, 55)

    fig.savefig("ratings_dist_hist.png")
    plt.show()

#call function
if __name__ == "__main__":
    main()
