import sys
import os
from urllib.parse import urlparse

import click

import soundcloud_degater.util.package_constants as const
import soundcloud_degater.util.selenium_wrapper as sw
from soundcloud_degater.util.exceptions import SoundCloudDegaterException
from soundcloud_degater.degaters.soundcloud_parse import SoundCloudParser
from soundcloud_degater.degaters.fanlink_parse import FanlinkParser


def validate_url(url: str):
    domain = urlparse(url).netloc
    if const.SC_domain not in domain:
        click.ClickException("Not a SoundCloud URL!")
        sys.exit()


def main(url: str, email: str, password: str, download_dir: str):
    validate_url(url)

    # Maybe move this to constants and expand on it later.
    kwargs = {
        'SC_client_id': const.SC_client_id,  # use mine later
        'process_names': 'heavy',  # heavy, light, or none processes Artist names so theres no BS full capitalized names
        'playlist_albums': True,  # group tracks in a playlist as an album if of right playlist type
    }

    scp = SoundCloudParser(**kwargs)
    call_type = scp.get_call_type(url)
    tracks_to_download = scp.get_track_list(call_type, url)
    driver = sw.new_driver()
    for track in tracks_to_download:
        purchase_url = track['purchase_url']
        print(f"Initiating degating for track: {track['title']} from {purchase_url}")
        if "fanlink.to" in purchase_url:
            parser = FanlinkParser(driver, email, password, download_dir)
        else:
            raise SoundCloudDegaterException("Not a gate we are able to handle. "
                                             "Please open a GitHub issue and we'll look into it.")

        download = parser.parse(purchase_url)


@click.command()
@click.argument('url')
@click.option('--email', '-e', help='The email to use when signing-in to social media.')
@click.option('--password', '-p', help='The password to use when signing-in to social media.')
@click.option('--download-dir', '-d', default=os.curdir,
              help="The directory to download files into. Defaults to current directory")
def cli(url, email, password, download_dir):
    main(url, email, password, download_dir)


if __name__ == "__main__":
    cli()
