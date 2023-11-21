from dotenv import load_dotenv
import os
from googleapiclient.discovery import build

load_dotenv()

DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=options,
        part="id,snippet",
        maxResults=1,
        type="video"
    ).execute()

    videos = []
    urls = []
    info = []

    for search_result in search_response.get('items', []):
        videos.append(search_result['snippet']['title'])
        info.append([search_result['id']["videoId"], search_result['snippet']['channelTitle']])

    for video in info:
        channelName = video[1].replace(" ", "")
        urls.append(f"https://www.youtube.com/watch?v={video[0]}_channel={channelName}")

    return urls[0]

