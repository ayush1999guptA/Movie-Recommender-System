import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def init():
    data = pd.read_csv("dataset/movies_metadata.csv")
    credits = pd.read_csv("dataset/credits.csv")
    keywords = pd.read_csv("dataset/keywords.csv")
    data = data.merge(credits, on='id')
    data = data.merge(keywords, on='id')
    data['genres'] = data['genres'].apply(literal_eval).apply(get_genres)
    data['cast'] = data['cast'].apply(literal_eval).apply(get_cast)
    data['crew'] = data['crew'].apply(literal_eval).apply(get_crew)
    data['keywords'] = data['keywords'].apply(literal_eval).apply(get_keywords)
    data['soup'] = data['genres']+data['cast']+data['crew']+data['keywords']
    data['soup'] = data['soup'].apply(lambda x: ' '.join(x))
    return data


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


def get_recommendation(data, similarity, title):
    titles = data[['title','vote_count','vote_average']]
    index = pd.Series(data.index, index=data['title'])
    try:
        ind = index[title]
        vote = data.iloc[ind]['vote_average']
        score = list(enumerate(similarity[ind]))
        score = sorted(score, key=lambda x: x[1], reverse=True)
        vote_min = vote - 2
        movie_indices = [i[0] for i in score]
        top = pd.DataFrame(titles.iloc[movie_indices])
        top = top[top['vote_average'] >= vote_min]
        top = top[1:]
        return top.head(10)
    except:
        return """Movie name not found. Please check spelling"""


def main():
    print("Creating Recommender...")
    data = init()
    print("Please Wait...")
    similarity = create_cosine_matrix(data)
    while(True):
        print("Type a Movie name")
        print("or Type Exit to exit")
        title = input()
        if title.lower() =="exit":
            break
        else:
            print(get_recommendation(data, similarity, title))


if __name__ == '__main__':
    main()
