import sys
from urllib.parse import urlparse
from soundcloud_parse import soundcloud_parser


def getDomain(url):
    split_url = url.split('/')

    if 'http' in url:
        del split_url[:2]

    return split_url[0]


if __name__ == "__main__":

    # arg parsing
    if len(sys.argv) == 2:
        (tmp, url) = sys.argv
        depth = 0

    else:
        print("Incorrect usage:\npython main url")
        sys.exit()

    kwargs = {
        'SC_client_id': 'a3dd183a357fcff9a6943c0d65664087',   # use mine later

        'process_names': 'heavy',       # heavy, light, or none     processes Artist names so theres no BS full capitalized names
        'playlist_albums': True,        # group tracks in a playlist as an album if of right playlist type
    }

    domain = urlparse(url).netloc

    # 'switch' based on domain type
    if 'soundcloud.com' in domain:
        scp = soundcloud_parser(**kwargs)
        scp.run(url)
    else:
        print('not soundcloud')
