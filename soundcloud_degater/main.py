import sys
from urllib.parse import urlparse

import click

import soundcloud_degater.package_constants as const
from soundcloud_degater.soundcloud_parse import SoundCloudParser


def validate_url(url: str):
    domain = urlparse(url).netloc
    if const.SC_domain not in domain:
        click.ClickException("Not a SoundCloud URL!")
    sys.exit()


def main(url, social, email, password):
    validate_url(url)
    kwargs = {
        'SC_client_id': const.SC_client_id,  # use mine later
        'process_names': 'heavy',  # heavy, light, or none processes Artist names so theres no BS full capitalized names
        'playlist_albums': True,  # group tracks in a playlist as an album if of right playlist type
    }
    scp = SoundCloudParser(**kwargs)
    scp.run(url)


@click.command()
@click.argument('url')
@click.option('--social', '-s', is_flag=True, default=False,
              help='Sign in to social media')
@click.option('--email', '-e', multiple=True, help='The email to use when signing-in to social media.')
@click.option('--password', '-p', multiple=True, help='The password to use when signing-in to social media.')
def cli(url, social, email, password):
    main(url, social, email, password)


