from spotify_token import get_token, get_auth_header
from requests import get
import json

def search_for_artist(token, artist_name):
    url="https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist found")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url=f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_users_playlists(token, user_id):
    url=f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

token = get_token()

while True:

    print("\n--Type exit at any time to leave program--\n")

    artist = input("Input an artist to find their top 10 songs: ")

    if artist.lower() == "exit":
        break

    find_artist = search_for_artist(token, artist)
    find_songs = get_songs_by_artist(token, find_artist["id"])

    for i, song in enumerate(find_songs):
        print(f"{i+1}. {song['name']}")