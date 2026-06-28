import requests
from pprint import pprint

API_KEY = 'a0cb1976025c8d6ceb2e3e9557601a7f'

# title, imdb id, poster_path, overview, release_date

# def search(query):
#     # query = 'Obsession'

#     r = requests.get(
#         "https://api.themoviedb.org/3/search/movie",
#         params={
#             "api_key": API_KEY,
#             "query": query
#         }
#     )

#     movies = r.json()["results"]


#     movielist = []
#     for movie in movies:
#         # print(movie["title"])
#         tmdb_id = movie['id']
#         imdburl = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids"
#         response = requests.get(imdburl, params={"api_key": API_KEY})
#         imdb_id  = response.json()['imdb_id']
#         #print(data)
#         movieobject = {'title' : movie['title'],
#                         'imdb_id' : imdb_id,
#                         'overview' : movie['overview'],
#                         'release_date' : movie['release_date'],
#                         'poster' : 'https://image.tmdb.org/t/p/w500' + str(movie['poster_path']),
#                         'vidsrc_url' : 'https://vidsrc-embed.ru/embed/movie/' + str(imdb_id)}
    
#         # print (movieobject)
#         movielist.append(movieobject)
#     return (movielist)

def search(query):
    r = requests.get(
        "https://api.themoviedb.org/3/search/multi",
        params={"api_key": API_KEY, "query": query}
    )

    results = r.json().get("results", [])

    filtered = []

    for item in results:
        if item["media_type"] not in ["movie", "tv"]:
            continue
        

        tmdb_id = item['id']
        media = item["media_type"]

        if media == "movie":
            ext_ids = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids"
        else:
            ext_ids = f"https://api.themoviedb.org/3/tv/{tmdb_id}/external_ids"

        imdb_id = requests.get(ext_ids, params={"api_key": API_KEY}).json()['imdb_id']

        # if media == 'movie':
        #     vidsrc_url = f'https://vidsrc-embed.ru/embed/movie/{imdb_id}/'
        # else:
        #     vidsrc_url = f'https://vidsrc-embed.ru/embed/tv/{imdb_id}/'

        filtered.append({
            "title": item.get("title") or item.get("name"),
            "media_type": item["media_type"],
            "tmdb_id": item["id"],
            "imdb_id" : imdb_id,
            "overview": item.get("overview"),
            "poster": "https://image.tmdb.org/t/p/w500" + item["poster_path"] if item.get("poster_path") else None,
            "vidsrc_url": f'https://vidsrc-embed.ru/embed/movie/{imdb_id}/'
        })

    return filtered




def get_tv_details(tv_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_id}"
    r = requests.get(url, params={"api_key": API_KEY})

    return r.json()

def get_imdb_id(tmdb_id):
    ext_ids = f"https://api.themoviedb.org/3/tv/{tmdb_id}/external_ids"
    imdb_id = requests.get(ext_ids, params={"api_key": API_KEY}).json()['imdb_id']

    return imdb_id



def get_popular():
    r = requests.get(
        "https://api.themoviedb.org/3/trending/all/day",
        params={"api_key": API_KEY}
    )

    results = r.json().get("results", [])

    filtered = []

    for item in results:
        if item["media_type"] not in ["movie", "tv"]:
            continue
        

        tmdb_id = item['id']
        media = item["media_type"]

        if media == "movie":
            ext_ids = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids"
        else:
            ext_ids = f"https://api.themoviedb.org/3/tv/{tmdb_id}/external_ids"

        imdb_id = requests.get(ext_ids, params={"api_key": API_KEY}).json()['imdb_id']

        # if media == 'movie':
        #     vidsrc_url = f'https://vidsrc-embed.ru/embed/movie/{imdb_id}/'
        # else:
        #     vidsrc_url = f'https://vidsrc-embed.ru/embed/tv/{imdb_id}/'

        filtered.append({
            "title": item.get("title") or item.get("name"),
            "media_type": item["media_type"],
            "tmdb_id": item["id"],
            "imdb_id" : imdb_id,
            "overview": item.get("overview"),
            "poster": "https://image.tmdb.org/t/p/w500" + item["poster_path"] if item.get("poster_path") else None,
            "vidsrc_url": f'https://vidsrc-embed.ru/embed/movie/{imdb_id}/'
        })

    return filtered




if __name__ == '__main__':
    pprint (get_tv_details('1418'))