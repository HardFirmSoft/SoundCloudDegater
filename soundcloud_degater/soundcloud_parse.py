from urllib.parse import urlparse
import string
import soundcloud


class soundcloud_parser(object):

    def __init__(self, **kwargs):

        self.client_id = kwargs['SC_client_id']

        self.process_names = kwargs['process_names']
        self.playlist_albums = kwargs['playlist_albums']

        self.album_types = ['album', 'demo', 'compilation']     # if playlist of these types, group as an album
        self.remix_types = ['remix', 'flip']                    # if any of these in the title of a track, process as a remix

        # this is the object that allows us to make easy soundcloud api calls
        self.client = soundcloud.Client(client_id=self.client_id)

    def run(self, url):

        call_type = self.get_call_type(url)

        if call_type == 'user':
            self.process_user(url)
        elif call_type == 'track':
            self.process_track(url)
        elif call_type == 'set':
            self.process_set(url)
        elif call_type == 'sets':
            self.process_sets(url)

    ###########################
    # Basic Process Functions
    ###########################

    def process_user(self, url):
        _user = self.get_user(url)
        _process_tracks = self.get_user_tracks(_user)
        self.download_tracks(_tracks)

    def track(self, url):
        _track = self.get_track(url)
        self.download_tracks([_track])

    def _process_set(self, url):
        _set = self.get_set(url)
        self.download_tracks(_set['tracks'])

    def _process_sets(self, url):
        _sets = self.get_sets(url)
        for _set in _sets:
            self.download_tracks(_set['tracks'])

    ##############
    # Call Types
    ##############

    def get_call_type(self, url):

        #   URL types
        #   user            https://soundcloud.com/xavi_real
        #   track           https://soundcloud.com/super7records/xavi-al-capone
        #   set/playlist    https://soundcloud.com/xavi_real/sets/al-capone

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

        print(path_splits)

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

    def download_sets(self, sets):
        for tracks in sets:
            self.download_tracks(tracks)

    def download_tracks(self, tracks):
        for track in tracks:
            self.download_track(track)

    def download_track(self, track):
        # to do
        # actually DOWNLOAD track

        print(track)
        pass

    ################
    # API requests
    ################

    def get_user(self, url):
        user = self.client.get('/resolve/', url=url)
        _user = self.dictionize_user(user)

        return _user

    def dictionize_user(self, user):
        _user = {
            'id': user.id,
            'username': user.username,
            'avatar_url': user.avatar_url,
        }

        return _user

    def get_track(self, url):

        track = self.client.get('/resolve/', url=url)
        user = self.client.get('/users/' + str(track.user_id))

        _user = self.dictionize_user(user)
        _track = self.dictionize_track(track, _user)

        return _track

    def get_user_tracks(self, _user):
        tracks = self.client.get('/users/' + str(_user['id']) + '/tracks/')

        _tracks = []
        for t in tracks:
            _track = self.dictionize_track(t, _user)
            _tracks.append(_track)

        return _tracks

    def dictionize_track(self, track, user):

        _track = {
            'id': track.id,
            'title': track.title,
            'album': '',
            'artist': user['username'],
            'album_artist': '',
            'year': track.created_at.split('/')[0],
            'artwork_url': track.artwork_url.replace('-large', '-t500x500') if track.artwork_url else user['avatar_url'].replace('-large', '-t500x500'),
            'purchase_url': track.purchase_url,
            'genre': track.genre,
            'bpm': track.bpm,
            'key_signature': track.key_signature,
        }

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
            elif any((x in _track['title'].lower()) for x in self.remix_types):    # remix with specified original artist
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

    def get_set(self, url):
        playlist = self.client.get('/resolve/', url=url)

        _playlist = {
            'id': playlist.id,
            'title': playlist.title,
            'artwork_url': playlist.artwork_url.replace('-large', '-t500x500') if playlist.artwork_url else None,
            'type': playlist.playlist_type,
            'tracks': [],
        }

        for t in playlist.tracks:
            # maybe this is unecessary, most of this info is already in
            # the playlist object, do a better job parsing that :P

            track = self.client.get('/tracks/' + str(t['id']))
            user = self.client.get('/users/' + str(track.user_id))

            _user = self.dictionize_user(user)
            _track = self.dictionize_track(track, _user)

            # change some tags because it's an album

            print(_playlist['type'])
            if self.playlist_albums and _playlist['type'] and any((x in _playlist['type']) for x in self.album_types):
                _track['album'] = _playlist['title']

                if not track.artwork_url and _playlist['artwork_url']:
                    _track['artwork_url'] = _playlist['artwork_url']

            _playlist['tracks'].append(_track)

        return _playlist

    def get_sets(self, url):
        # this is elegant
        # but uses WAYYYY too many fucking API calls lol
        # maybe do something about this

        playlists = self.client.get('/resolve/', url=url)

        _playlists = []
        for p in playlists:
            print(p.permalink_url)
            _playlists.append(self.get_set(p.permalink_url))

        return _playlists
