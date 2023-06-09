from src.mixin_api import APIMixin
from pprint import pprint


class Video(APIMixin):
    def __init__(self, video_id: str) -> None:
        try:
            self.video_id = video_id
            self.video_response = self.get_service().videos().list(
                                                                   part='snippet,statistics,contentDetails,topicDetails',
                                                                   id=video_id
                                                                   ).execute()
            self.title: str = self.video_response['items'][0]['snippet']['localized']["title"]
            self.video_url: str = self.video_response['items'][0]['snippet']['thumbnails']['default']['url']
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video_id = video_id
            self.title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

