import pandas as pd
from ast import literal_eval


def init():
    data = pd.read_csv("dataset/movies_metadata.csv")
    data['genres'] = data['genres'].apply(literal_eval).apply(get_genres)
    return data


def get_mean(data):
    count = data['vote_count'].sum()
    rating = data['vote_average']*data['vote_count']
    rate = rating.sum()
    C = rate/count
    return C


def get_genre_list(data):
    genres = set(x for l in data['genres'] for x in l)
    return list(genres)


def get_genres(x):
    genre = []
    if isinstance(x,list):
        for i in x:
            genre.append(i['name'])
    return genre


def get_top(data, C):
    m = 500
    top = data[data['vote_count'] > 500]
    print(C)
    top = top[['title','genres','vote_count','vote_average']]
    top['rating'] = (top['vote_count']/(top['vote_count']+m))*top['vote_average']+(m/(top['vote_count']+m))*C
    top = top.sort_values(by=['rating'], ascending=False)
    return top.head(20)


def top_list(data, genre, C):
    top = data[data['genres'].apply(lambda x: genre in x)]
    if top.empty:
        print("Please check Genre Name")
        return get_genre_list(data)
    top = top[['title','release_date','vote_count','vote_average']]
    top = top.sort_values(by='vote_count', ascending = False)
    top = top[:50]
    m = top['vote_count'].min()
    top['rating'] = (top['vote_count']/(top['vote_count']+m))*top['vote_average']+(m/(top['vote_count']+m))*C
    top = top.sort_values(by=['rating'], ascending=False)
    return top.head(10)


def main():
    data = init()
    C = get_mean(data)
    print(get_genre_list(data))
    while(True):
        print("Type All for top list")
        print("or Choose a genre from genre list")
        print("or Type Exit to exit")
        genre = input()
        genre = genre.title()
        if genre == "All":
            print(get_top(data, C))
        elif genre == "Exit":
            break
        else:
            print(top_list(data, genre, C))

if __name__ == '__main__':
    main()
