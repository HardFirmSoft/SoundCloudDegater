import sys
from urllib.parse import urlparse

import click

import soundcloud_degater.util.package_constants as const
from soundcloud_degater.degaters.soundcloud_parse import SoundCloudParser
from soundcloud_degater.degaters.fanlink_parse import FanlinkParser


def validate_url(url: str):
    domain = urlparse(url).netloc
    if const.SC_domain not in domain:
        click.ClickException("Not a SoundCloud URL!")
        sys.exit()


def main(url, social, email, password):
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

    for track in tracks_to_download:
        purchase_url = track['purchase_url']

        if "fanlink.to" in purchase_url:
            parser = FanlinkParser()
        else:
            parser = None

        download = parser.parse(purchase_url)
        print(download)


@click.command()
@click.argument('url')
@click.option('--social', '-s', is_flag=True, default=False,
              help='Sign in to social media')
@click.option('--email', '-e', multiple=True, help='The email to use when signing-in to social media.')
@click.option('--password', '-p', multiple=True, help='The password to use when signing-in to social media.')
def cli(url, social, email, password):
    main(url, social, email, password)


if __name__ == "__main__":
    cli()