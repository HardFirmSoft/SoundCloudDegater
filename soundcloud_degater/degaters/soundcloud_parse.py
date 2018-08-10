import string
from typing import List, Dict
from urllib.parse import urlparse

import soundcloud

from soundcloud_degater.degaters.fanlink_parse import FanlinkParser

"TODO: better error handling, if 404 returned, throws Error."


class SoundCloudParser(object):
    """Class for processing SoundCloud data."""

    def __init__(self, **kwargs):
        self.client_id = kwargs['SC_client_id']

        self.process_names = kwargs['process_names']
        self.playlist_albums = kwargs['playlist_albums']

        # if playlist of these types, group as an album
        self.album_types = ['album', 'compilation', 'demo', 'ep']
        # if any of these words are in the title of a track, process as a remix
        self.remix_types = ['remix', 'flip']

        # this is the object that allows us to make easy soundcloud api calls
        self.sc_client = soundcloud.Client(client_id=self.client_id)

    ###########################
    # Basic Process Functions
    ###########################

    def get_track_list(self, call_type: str, url: str) -> List[Dict]:
        """Depending on the call type, get list of tracks."""
        tracks = []

        if call_type == 'user':
            tracks += self.get_user_tracks(self.get_user(url))
        elif call_type == 'track':
            tracks.append(self.get_track(url))
        elif call_type == 'set':
            tracks += self.get_set(url)['tracks']
        elif call_type == 'sets':
            tracks += [track for track in [set['tracks'] for set in self.get_sets(url)]]
        return tracks

    ##############
    # Call Types
    ##############
    @staticmethod
    def get_call_type(url):

        #   URL types
        #   user            https://soundcloud.com/xavi_real
        #   track           https://soundcloud.com/super7records/xavi-al-capone
        #   set/playlist    https://soundcloud.com/xavi_real/sets/al-capone
        #   sets            https://soundcloud.com/xavi_real/sets

        #   /user/sets/set_name
        #   OR
        #   /user/track

        path = urlparse(url).path

        path_splits = path.split('/')

        # remove blank spaces from path_splits
        i = 0
        while i < len(path_splits):
            if path_splits[i] == '':
                i -= 1
                del path_splits[i + 1]
            i += 1

        if len(path_splits) == 1:
            return 'user'
        elif len(path_splits) == 2:

            if path_splits[1] == 'sets':
                return 'sets'

            else:
                return 'track'
        elif len(path_splits) == 3:
            return 'set'

    ###############
    # Downloaders
    ###############

    ################
    # API requests
    ################

    def get_user(self, url: str) -> dict:
        user = self.sc_client.get('/resolve/', url=url)
        _user = self.dictionize_user_obj(user)
        return _user

    def get_track(self, url: str) -> dict:
        track = self.sc_client.get('/resolve/', url=url)
        _user = self.redictionize_user(track.user)
        _track = self.dictionize_track_obj(track, _user)
        return _track

    def get_user_tracks(self, _user: dict) -> List[Dict]:
        tracks = self.sc_client.get('/users/' + str(_user['id']) + '/tracks/')
        _tracks = []

        for t in tracks:
            _track = self.dictionize_track_obj(t, _user)
            _tracks.append(_track)
        return _tracks

    def get_set(self, url: str) -> dict:
        playlist = self.sc_client.get('/resolve/', url=url)
        _playlist = self.dictionize_set_obj(playlist)
        return _playlist

    def get_sets(self, url: str) -> List[Dict]:
        playlists = self.sc_client.get('/resolve/', url=url)
        _playlists = self.dictionize_sets(playlists)
        return _playlists

    #######################
    # Dictionary Builders
    #######################
    @staticmethod
    def dictionize_user_obj(user) -> dict:
        _user = {
            'id': user.id,
            'username': user.username,
            'avatar_url': user.avatar_url.replace('-large', '-t500x500'),
        }

        return _user

    @staticmethod
    def redictionize_user(user: dict) -> dict:
        # useful when the miniuser is already there from another api call
        _user = {
            'id': user['id'],
            'username': user['username'],
            'avatar_url': user['avatar_url'].replace('-large', '-t500x500'),
        }

        return _user

    def dictionize_track_obj(self, track, user: dict) -> dict:
        _track = {
            'id': track.id,
            'title': track.title,
            'album': 'Soundcloud',
            'artist': user['username'],
            'album_artist': '',
            'year': track.created_at.split('/')[0],
            'artwork_url': track.artwork_url.replace('-large', '-t500x500') if track.artwork_url else user['avatar_url'],
            'purchase_url': track.purchase_url,
            'genre': track.genre,
            'bpm': track.bpm,
            'key_signature': track.key_signature,
        }

        return self.track_processing(_track)

    def redictionize_track(self, track: dict, user: dict) -> dict:
        _track = {
            'id': track['id'],
            'title': track['title'],
            'album': 'Soundcloud',
            'artist': user['username'],
            'album_artist': '',
            'year': track['created_at'].split('/')[0],
            'artwork_url': track['artwork_url'].replace('-large', '-t500x500') if track['artwork_url'] else user['avatar_url'],
            'purchase_url': track['purchase_url'],
            'genre': track['genre'],
            'bpm': track['bpm'],
            'key_signature': track['key_signature'],
        }

        return self.track_processing(_track)

    def dictionize_set_obj(self, playlist) -> dict:
        _playlist = {
            'id': playlist.id,
            'title': playlist.title,
            'artwork_url': playlist.artwork_url.replace('-large', '-t500x500') if playlist.artwork_url else None,
            'type': playlist.playlist_type,
            'tracks': [],
        }

        for track in playlist.tracks:
            # maybe this is unecessary, most of this info is already in
            # the playlist object, do a better job parsing that :P

            _user = self.redictionize_user(track['user'])
            _track = self.redictionize_track(track, _user)

            # change some tags because it's an album
            if self.playlist_albums and _playlist['type'] and any((x in _playlist['type']) for x in self.album_types):
                _track['album'] = _playlist['title']

                if not _track['artwork_url'] and _playlist['artwork_url']:
                    _track['artwork_url'] = _playlist['artwork_url']

            _playlist['tracks'].append(_track)

        return _playlist

    def dictionize_sets(self, playlists: List[Dict]) -> List[Dict]:
        _playlists = []
        for playlist in playlists:
            _playlist = self.dictionize_set_obj(playlist)
            _playlists.append(_playlist)

        return _playlists

    #########################
    # Dictionary Processing
    #########################

    def track_processing(self, _track: dict) -> dict:
        # naming weirdness because Im a weirdo
        # who really cares about this for some reason

        if self.process_names == 'heavy':
            _track['artist'] = string.capwords(' '.join(_track['artist'].split()).lower())
        elif self.process_names == 'light':
            _track['artist'] = ' '.join(_track['artist'].split())

        if '-' in _track['title']:
            new_artist, title = _track['title'].split('-', 1)
            old_artist = _track['artist']

            if self.process_names == 'heavy':
                new_artist = string.capwords(' '.join(new_artist.split()).lower())
            elif self.process_names == 'light':
                new_artist = ' '.join(new_artist.split())

            # check if name is the same
            if old_artist.lower() == new_artist.lower():        # Double titled
                _track['title'] = title.strip()
            elif old_artist.lower() in new_artist.lower():      # Collab
                _track['title'] = title.strip()
                _track['album'] = 'Collabs'
                _track['artist'] = new_artist
                _track['album_artist'] = old_artist
            elif any((x in _track['title'].lower()) for x in self.remix_types):   # remix with specified original artist
                _track['title'] = title.strip()
                _track['album'] = 'Remixes'
                _track['artist'] = new_artist
                _track['album_artist'] = old_artist
            else:                                                                   # published by someone else maybe
                _track['title'] = title.strip()
                _track['artist'] = new_artist

        elif any((x in _track['title'].lower()) for x in self.remix_types):        # remix without an original artist
            _track['album'] = 'Remixes'
            _track['album_artist'] = _track['artist']

        return _track
