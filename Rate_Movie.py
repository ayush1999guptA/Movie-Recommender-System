import pandas as pd
import csv


def init():
    data = pd.read_csv("dataset/movies_metadata.csv")
    return data


def add_rating(data, userId, title, rating):
    if rating>5 or rating<=0:
        print("rating should be between 0-5")
        return
    try:
        ind = data[data['title'] == title].id.item()
        row = [userId, ind, rating]
        with open('dataset/ratings.csv','a') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        print("Movie Rated Successfully")
    except:
        print("No movie found with this name")


def main():
    data = init()
    print("Enter exit anywhere to exit")
    while(True):
        userId = input("Enter userId: ")
        if userId.lower() == "exit":
            break
        userId = int(userId)
        title = input("Enter movie name: ")
        if title.lower() == "exit":
            break
        rating = input("Enter rating: ")
        if rating.lower() == "exit":
            break
        rating = float(rating)
        add_rating(data, userId, title, rating)


if __name__ == '__main__':
    main()
