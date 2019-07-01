import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader, Dataset, SVD, evaluate


def init():
    data = pd.read_csv("dataset/movies_metadata.csv")
    credits = pd.read_csv("dataset/credits.csv")
    keywords = pd.read_csv("dataset/keywords.csv")
    ratings = pd.read_csv("dataset/ratings.csv")
    data = data.merge(credits, on='id')
    data = data.merge(keywords, on='id')
    data['genres'] = data['genres'].apply(literal_eval).apply(get_genres)
    data['cast'] = data['cast'].apply(literal_eval).apply(get_cast)
    data['crew'] = data['crew'].apply(literal_eval).apply(get_crew)
    data['keywords'] = data['keywords'].apply(literal_eval).apply(get_keywords)
    data['soup'] = data['genres']+data['cast']+data['crew']+data['keywords']
    data['soup'] = data['soup'].apply(lambda x: ' '.join(x))
    return data, ratings


def get_genres(x):
    genre = []
    for i in x:
        genre.append(i['name'])
    return genre


def get_cast(x):
    cast = []
    num = 0
    for i in x:
        i['name'] = i['name'].replace(" ","")
        cast.append(i['name'])
        num = num + 1
        if num==5:
            break
    return cast


def get_crew(x):
    crew = []
    for i in x:
        if i['job'] == 'Director' or i['job'] =='Screenplay':
            i['name'] = i['name'].replace(" ","")
            crew.append(i['name'])
    return crew


def get_keywords(x):
    keywords = []
    for i in x:
        i['name'] = i['name'].replace(" ","")
        keywords.append(i['name'])
    return keywords


def create_cosine_matrix(data):
    count = CountVectorizer(analyzer='word', stop_words='english')
    matrix = count.fit_transform(data['soup'])
    similarity = cosine_similarity(matrix,matrix)
    return similarity


def train_data(ratings):
    reader = Reader()
    dataset = Dataset.load_from_df(ratings, reader)
    dataset.split(n_folds=5)
    svd = SVD()
    trainset = dataset.build_full_trainset()
    svd.fit(trainset)
    return svd


def get_movie_list(index, similarity, movieId):
    ind = index[movieId]
    score = list(enumerate(similarity[ind]))
    score = sorted(score, key=lambda x: x[1], reverse=True)
    score = score[0:11]
    movie_indices = [i[0] for i in score]
    return movie_indices


def get_recommendation(data, ratings, similarity, svd, userId):
    titles = data[['title','vote_count','id','vote_average']]
    index = pd.Series(data.index, index = data['id'])

    userdata = ratings[ratings['userId'] == userId]
    userdata = userdata[userdata['rating'] >= 2.5]
    if userdata.empty == True:
        print("Insufficient Data Present")
        return

    movie = set()
    for i in userdata['movieId']:
        movies = get_movie_list(index, similarity, i)
        for x in movies:
            movie.add(x)
    for i in userdata['movieId']:
        movie.remove(index[i])

    movie_indices = list(movie)
    top = pd.DataFrame(titles.iloc[movie_indices])
    top['prediction'] = top['id'].apply(lambda x: svd.predict(userId, x).est)
    top = top[top['vote_average'] >= 5]
    top = top.sort_values(by=['prediction','vote_average'], ascending=False)
    return top.head(15)


def main():
    print("Creating Recommender...")
    data, ratings = init()
    print("Please Wait...")
    similarity = create_cosine_matrix(data)
    svd = train_data(ratings)
    userId = int(input("Enter your user id: "))
    print(get_recommendation(data, ratings, similarity, svd, userId))


if __name__ == '__main__':
    main()
