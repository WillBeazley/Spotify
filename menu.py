from spotifyExtractor import search_for_artist, get_songs_by_artist, get_token
from googleExtractor import youtube_search
from pprint import pprint
import inquirer
from pytube import YouTube

token = get_token()

while True:

    print("\n--Type exit at any time to leave program--\n")

    artist = input("Input an artist to find their top 10 songs: ")

    if artist.lower() == "exit":
        break

    find_artist = search_for_artist(token, artist)
    find_songs = get_songs_by_artist(token, find_artist["id"])

    choices = []
    songID = {}

    for song in find_songs:
        choices.append(song["name"])
        songID[song["name"]] = song["id"]

    questions = [
        inquirer.List(
            "song",
            message="Here are their songs, please select one for further details:",
            choices=choices,
        ),
    ]

    song_choice = inquirer.prompt(questions)

    url = youtube_search(song_choice["song"])

    YouTube(url).streams.filter(progressive=True).get_highest_resolution().download("Downloads")

    print(f"{url} successfully downloaded")