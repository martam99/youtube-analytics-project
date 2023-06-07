import datetime
import isodate
from src.mixin_api import APIMixin


class PlayList(APIMixin):
    """Класс для плейлиста на Ютубе"""

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist = self.get_service().playlists().list(id=playlist_id,
                                                            part='snippet, contentDetails',
                                                            ).execute()
        self.title = self.playlist['items'][0]['snippet']['localized']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    @property
    def total_duration(self):
        """Получаем данные по видеороликам в плейлисте"""
        time_list = []
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        # Получаем все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        # Выводим длительности видеороликов из плейлиста с суммарной длительностью
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
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
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids),
                                                    ).execute()

        like_list = []
        for el in video_response['items']:
            likes = el['statistics']['likeCount']
            like_list.append(likes)
        max_like_count = max(like_list)

        if likes == max_like_count:
            return f"https://youtu.be/{el['id']}"

