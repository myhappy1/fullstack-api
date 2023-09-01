
import pandas as pd
import requests
import sys
from tqdm import tqdm
import time
def add_url(row):
    return f'https://www.imdb.com/title/tt{row}/'

def add_rating(df):
    ratings_df = pd.read_csv('data/ratings.csv')
    ratings_df['movieId'] = ratings_df['movieId'].astype(str)
    agg_df = ratings_df.groupby('movieId').agg(
        ratings_count = ('rating','count'),
        ratings_avf = ('rating','mean')
    ).reset_index()
    
    ratings__added_df  = df.merge(agg_df,on='movieId')
    return ratings__added_df

def add_poster(df):
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        tmdb_id = row['tmdbId']
        tmdb_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key=0d1228a6e3b2e2cbd8dd8c61420346c5&language=en-US"
        result = requests.get(tmdb_url)
        
        try:
            df.at[i,"poster_path"] = "https://image.tmdb.org/t/p/original" + result.json()['poster_path']
            time.sleep(0,1)
        except (TypeError,KeyError) as e:
            df.at[i,"poster_path"] = "https://image.tmdb.org/t/p/original/uXDfJbP4ijW5hWSBrPrlKpxab.jpg"
    return df

if __name__ =="__main__":
    movie_df = pd.read_csv('data/movies.csv')
    #ID를 문자로 인식하게 만든다.
    movie_df['movieId'] = movie_df['movieId'].astype(str)
    links_df = pd.read_csv('data/links.csv',dtype=str)
    merged_df = movie_df.merge(links_df,on='movieId', how='left')
    merged_df['url'] = merged_df['imdbId'].apply(lambda x : add_url(x))
    result_df = add_rating(merged_df)
    result_df["poster_path"] = None
    result_df = add_poster(result_df)
    result_df.to_csv("data/movies_final.csv",index=None)
    