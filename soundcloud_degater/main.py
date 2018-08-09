import sys
from urllib.parse import urlparse

import util.package_constants as const

from degaters.soundcloud_parse import SoundCloudParser
import util.selenium_wrapper as sw


def get_domain(url: str) -> str:
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
        const.logger.error("Usage:\npython main url")
        sys.exit()

    kwargs = {
        'SC_client_id': const.SC_client_id,   # use mine later
        'process_names': 'heavy',       # heavy, light, or none processes Artist names so theres no BS full capitalized names
        'playlist_albums': True,        # group tracks in a playlist as an album if of right playlist type
    }

    domain = urlparse(url).netloc

    sw.generate_driver()   # start webdriver
    print(sw.driver)

    # 'switch' based on domain type
    if const.SC_domain in domain:
        scp = SoundCloudParser(**kwargs)
        scp.run(url)
    else:
        const.logger.error("Provided URL is not a valid SoundCloud URL.")
