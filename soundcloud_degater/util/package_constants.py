import logging

# To be better handled once CLI is implemented
logger = logging.getLogger()

# SoundCloud stuff
SC_client_id = 'a3dd183a357fcff9a6943c0d65664087'
SC_domain = 'soundcloud.com'

# login creds
SC_email = 'Swift142'
SC_password = 'July2413SC'

# toneden access soundcloud
SC_access_toneden = "https://soundcloud.com/connect?response_type=code&redirect_uri=https%3A%2F%2Fwww.toneden.io%2Fauth%2Fsoundcloud%2Fcallback&client_id=0e545f4886c0c8006a4f95e2036399c0"
# FB_em =
# FB_pw =

# Fanlink CSS Constants
FL_first_button_class = 'link-option-row-title'
FL_second_button_class = 'post-gate-btn'


# Generic constants
free_download = 'FREE DOWNLOAD'
sound_cloud_follow = 'FOLLOW ON SOUNDCLOUD'

# Sites we are able to download from.

fanlink = "fanlink.to"
handled_sites = [
    fanlink,
]


timeout = 10
