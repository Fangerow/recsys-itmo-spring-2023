from .random import Random
from .recommender import Recommender
from .sticky_artist import StickyArtist
import random


class ContextualCustom(Recommender):
    """
    Recommend tracks closest to the previous one.
    Fall back to the random recommender if no
    recommendations found for the track.
    """

    def __init__(self, tracks_redis, catalog, artists, first):
        self.tracks_redis = tracks_redis
        self.fallback = StickyArtist(tracks_redis, artists, catalog)
        self.catalog = catalog
        self.first = first

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        start_track_from_redis = self.tracks_redis.get(self.first[user])
        if start_track_from_redis is None:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        # previous_track = self.catalog.from_bytes(previous_track)
        recommendations = self.catalog.from_bytes(start_track_from_redis).recommendations
        if not recommendations:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        shuffled = list(recommendations)
        random.shuffle(shuffled)
        return shuffled[0]
# class ContextualCustom(Recommender):
#     """
#     Recommend tracks closest to the previous one.
#     Fall back to the random recommender if no
#     recommendations found for the track.
#     """
#
#     def __init__(self, tracks_redis, artists_redis, catalog, first_track):
#         self.tracks_redis = tracks_redis
#         self.fallback = Random(tracks_redis)# StickyArtist(tracks_redis, artists_redis, catalog)
#         self.catalog = catalog
#         self.first = first_track
#
#     def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
#         previous_track = self.tracks_redis.get(prev_track)
#         if previous_track is None:
#             return self.fallback.recommend_next(user, prev_track, prev_track_time)
#
#         previous_track = self.catalog.from_bytes(previous_track)
#         recommendations = previous_track.recommendations
#         if not recommendations:
#             return self.fallback.recommend_next(user, prev_track, prev_track_time)
#
#         shuffled = list(recommendations)
#         random.shuffle(shuffled)
#         return shuffled[0]

