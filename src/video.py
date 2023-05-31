import os
from googleapiclient.discovery import build
from pprint import pprint


class Video:
    api_key: str = os.getenv('YT-API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=video_id
                                                         ).execute()
        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.video_url: str = self.video_response['items'][0]['snippet']['thumbnails']['default']['url']
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
