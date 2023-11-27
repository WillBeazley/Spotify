from spotifyExtractor import search_for_artist, get_songs_by_artist, get_token, search_for_playlist, get_playlist
from googleExtractor import youtube_search
from pprint import pprint
import inquirer
from pytube import YouTube
import time

token = get_token()

def playlists(search):

    result = search_for_playlist(token, search)

    if result == None:
        return None

    playlists = []

    for playlist in result:
        playlists.append(playlist["name"])

    choices = []
    playlistDetails = {}

    for playlist in result:
        choices.append(playlist['name'])
        playlistDetails[playlist["name"]] = playlist["id"]

    choices.append("none")

    questions = [
        inquirer.List(
            "playlist",
            message="Here are the playlists, please select one for further details",
            choices=choices,
        ),
    ]

    playlist_choice = inquirer.prompt(questions)

    if playlist_choice["playlist"] == "none":
        return None

    tracks = get_playlist(token, playlistDetails[playlist_choice["playlist"]])

    for i, track in enumerate(tracks):
        artist_name = track["track"]["artists"][0]["name"]
        song_name = track["track"]["name"]

        url = youtube_search(f"{song_name}, {artist_name}")

        print(f"Downloading song {i+1}: {song_name} by {artist_name}")

        YouTube(url).streams.filter(progressive=True).get_highest_resolution().download(f"Downloads/{playlist_choice['playlist']}")

        time.sleep(3)


    return playlist_choice

def artists(artist):

    if artist.lower() == "exit":
        return None

    find_artist = search_for_artist(token, artist)

    if find_artist == None:
        return None

    find_songs = get_songs_by_artist(token, find_artist["id"])

    choices = []
    songID = {}

    for song in find_songs:
        choices.append(song["name"])
        songID[song["name"]] = song["id"]

    choices.append("none")

    questions = [
        inquirer.List(
            "song",
            message="Here are their songs, please select one for further details",
            choices=choices,
        ),
    ]

    song_choice = inquirer.prompt(questions)

    if song_choice["song"] == None:
        return None
    

    url = youtube_search(f"{song_choice['song']}, {artist}")

    YouTube(url).streams.filter(progressive=True).get_highest_resolution().download("Downloads")

    print(f"{url} successfully downloaded")

    return song_choice

while True:

    type = [
        inquirer.List(
            "type",
            message="Would you like to download a playlist or song?",
            choices=["Playlist", "Song", "Exit"],
        )
    ]

    decision = inquirer.prompt(type)

    if decision["type"] == "Song":

        artist = input("Input an artist to find their top 10 songs: ")

        song_choice = artists(artist)

        if song_choice == None:
            print()
            continue

    if decision["type"] == "Playlist":
        
        playlist = input("Input a playlist you would like to search for: ")

        playlist_choice = playlists(playlist)

        if playlist_choice == None:
            print()
            continue

    if decision["type"] == "Exit":
        break

        
