from typing import List, Dict

import soundcloud_degater.util.package_constants as const
import soundcloud_degater.util.selenium_wrapper as sw

# from exceptions import SoundCloudDegaterException


class FanlinkParser(object):

    def __init__(self, social_connector='facebook'):
        self.timeout = 5
        self.social_connector = social_connector

    def parse(self, url):
        sw.get(url)
        self.layer1_home()  # begin traversal

        print('complete')
        raise Exception

    ########################
    # Sequential Traversal
    ########################

    def layer1_home(self):
        # click 'free download' (one of many options)

        buttons = sw.filt_els_by_text('CLASS_NAME', 'link-option-row-action', 'FREE DOWNLOAD')
        if buttons:
            sw.click(buttons[0])
            self.layer2_single_download()
        else:
            self.layer2_single_download()    # fanlink sometimes might begin in layer2

    def layer2_single_download(self):
        # click 'free download' (only option)
        buttons = sw.filt_els_by_text('CLASS_NAME', 'post-gate-btn', 'FREE DOWNLOAD')
        if buttons:
            sw.click(buttons[0])
            self.layer3_follow_SC()
        else:
            self.fail()

    def layer3_follow_SC(self):
        # click 'follow on soundcloud'
        buttons = sw.filt_els_by_text('CLASS_NAME', 'soundcloud', 'FOLLOW ON SOUNDCLOUD')
        if buttons:
            sw.click(buttons[0])
            self.layer4_give_SC_access()
        else:
            self.fail()

    def layer4_give_SC_access(self):
        # in new window, click on FB signup
        sw.get(const.SC_access_toneden)
        social_buttons = sw.get_elements_with_wait('PARTIAL_LINK_TEXT', 'Sign in with Facebook')
        if social_buttons:
            sw.click(social_buttons[0])
            self.layer5_sign_into_FB()
        else:
            self.fail()

    def layer5_sign_into_FB(self):

        pass

    # Definitely need to improve on this.
    def fail(self):
        print('failed')
        raise Exception

    ###########
    # Utility
    ###########
