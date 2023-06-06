import datetime
import os
from googleapiclient.discovery import build
import isodate


class PlayList:
    """Класс для плейлиста на Ютубе"""
    api_key: str = os.getenv('YT-API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist = self.youtube.playlists().list(id=playlist_id,
                                                      part='snippet, contentDetails',
                                                      ).execute()
        self.title = self.playlist['items'][0]['snippet']['localized']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    @property
    def total_duration(self):
        """Получаем данные по видеороликам в плейлисте"""
        time_list = []
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        # Получаем все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        # Выводим длительности видеороликов из плейлиста с суммарной длительностью
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time_list.append(duration)
        total_time = sum(time_list, datetime.timedelta())
        return total_time

    def show_best_video(self):
        """Метод выводит самое популярное видео из плейлиста"""
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids),
                                                    ).execute()

        like_list = []
        for el in video_response['items']:
            likes = el['statistics']['likeCount']
            like_list.append(likes)
        max_like_count = max(like_list)

        if likes == max_like_count:
            return f"https://youtu.be/{el['id']}"

