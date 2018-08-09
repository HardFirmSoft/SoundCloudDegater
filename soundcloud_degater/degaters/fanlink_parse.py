from typing import List, Dict

import util.package_constants as const
import util.selenium_wrapper as sw


from contextlib import contextmanager


# from exceptions import SoundCloudDegaterException


class FanlinkParser(object):

    def __init__(self):
        self.timeout = 5

        self.social_connector = 'facebook'

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
        # self.gen_html_file(str(self.driver.page_source))

        buttons = sw.filt_els_by_text('CLASS_NAME', 'link-option-row-action', 'FREE DOWNLOAD')
        if buttons:
            sw.click(buttons[0])
            self.layer2_singleDownload()
        else:
            self.layer2_singleDownload()    # fanlink sometimes might begin in layer2

    def layer2_singleDownload(self):
        # click 'free download' (only option)
        buttons = sw.filt_els_by_text('CLASS_NAME', 'post-gate-btn', 'FREE DOWNLOAD')
        if buttons:
            sw.click(buttons[0])
            self.layer3_followSC()
        else:
            self.fail()

    def layer3_followSC(self):
        # click 'follow on soundcloud'
        buttons = sw.filt_els_by_text('CLASS_NAME', 'soundcloud', 'FOLLOW ON SOUNDCLOUD')
        if buttons:
            sw.click(buttons[0])
            self.layer4_give_SC_access()
        else:
            self.fail()

    def layer4_give_SC_access(self):
        # in new window, click on FB signup
        social_buttons = sw.get_els_by('CLASS_NAME', 'connect-social-buttons')
        if social_buttons:
            for button in social_buttons:
                if self.social_connector in button.CLASS_NAME:
                    sw.click(button)
                    break

            self.layer5()
        else:
            self.fail()

    def layer5_sign_into_FB(self):

        pass

    def fail(self):
        print('failed')
        raise Exception

    ###########
    # Utility
    ###########
