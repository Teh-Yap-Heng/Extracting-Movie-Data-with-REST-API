import requests_with_caching
import json

def get_movies_from_tastedive(movie):
    baseurl = 'https://tastedive.com/api/similar'
    para_dict = {}
    para_dict['q'] = movie
    para_dict['type'] = 'movies'
    para_dict['limit'] = 5
    td_resp = requests_with_caching.get(baseurl, params = para_dict)
    return td_resp.json()

def extract_movie_titles(dic):
    return [info['Name'] for info in dic['Similar']['Results']]

def get_related_titles(lst):
    new_lst = []
    for item in lst:
        dic = get_movies_from_tastedive(item)
        for name in extract_movie_titles(dic):
            new_lst.append(name)
    return list(set(new_lst))

def get_movie_data(movie):
    baseurl = 'http://www.omdbapi.com/'
    para_dict = {}
    para_dict['t'] = movie
    para_dict['r'] = 'json'
    omdb_resp = requests_with_caching.get(baseurl, params = para_dict)
    return omdb_resp.json()

def get_movie_rating(dic):
    for rate in dic['Ratings']:
        if rate['Source'] == 'Rotten Tomatoes':
            return int(rate['Value'][0:2])
    return 0

def get_sorted_recommendations(lst):
    rate_lst = []
    movie_dic = {}
    movie_lst = get_related_titles(lst)
    for movie in movie_lst:
        dic = get_movie_data(movie)
        rating = get_movie_rating(dic)
        movie_dic[movie] = rating
    return sorted([movie for movie in movie_dic], key = lambda movie: -movie_dic[movie])

print(get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"]))