import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT-API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = self.channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscribers = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.total_views = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title}({self.url})"

    def __add__(self, other):
        return int(self.total_views) + int(other.total_views)

    def __sub__(self, other):
        return int(self.total_views) - int(other.total_views)

    def __gt__(self, other):
        return int(self.total_views) > int(other.total_views)

    def __ge__(self, other):
        return int(self.total_views) >= int(other.total_views)

    def __le__(self, other):
        return int(self.total_views) < int(other.total_views)

    def __lt__(self, other):
        return int(self.total_views) <= int(other.total_views)

    def __eq__(self, other):
        return int(self.total_views) == int(other.total_views)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute(), indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return Channel.youtube

    def to_json(self, file_name):
        json_dict = {'channel_id': self.channel_id,
                     'title': self.title,
                     'description': self.description,
                     'url': self.url,
                     'subscribers': self.subscribers,
                     'video_count': self.video_count,
                     'total_views': self.total_views
                     }
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(json.dumps(json_dict, indent=2, ensure_ascii=False))


