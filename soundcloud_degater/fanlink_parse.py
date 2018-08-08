from typing import List, Dict

import package_constants as const
from exceptions import SoundCloudDegaterException

from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time


class FanlinkParser(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.timeout = 5

        self.social_connector = 'facebook'

    def parse(self, url):

        self.driver.get(url)
        self.layer1_home()  # begin traversal

        print('complete')
        raise Exception

    ########################
    # Sequential Traversal
    ########################

    def layer1_home(self):
        # click 'free download' (one of many options)
        self.gen_html_file(str(self.driver.page_source))

        buttons = self.filt_els_by_text('link-option-row-action', 'FREE DOWNLOAD')
        if buttons:
            self.click(buttons[0])
            self.layer2_singleDownload()
        else:
            self.layer2_singleDownload()    # fanlink sometimes might begin in layer2

    def layer2_singleDownload(self):
        # click 'free download' (only option)
        buttons = self.filt_els_by_text('post-gate-btn', 'FREE DOWNLOAD')
        if buttons:
            self.click(buttons[0])
            self.layer3_followSC()
        else:
            self.fail()

    def layer3_followSC(self):
        # click 'follow on soundcloud'
        buttons = self.filt_els_by_text('soundcloud', 'FOLLOW ON SOUNDCLOUD')
        if buttons:
            self.click(buttons[0])
            self.layer4_give_SC_access()
        else:
            self.fail()

    def layer4_give_SC_access(self):
        # in new window, click on FB signup
        social_buttons = self.get_els_by_class('connect-social-buttons')
        if social_buttons:
            for button in social_buttons:
                if self.social_connector in button.CLASS_NAME:
                    self.click(button)
                    break

            self.layer5()
        else:
            self.fail()

    def layer5_sign_into_FB(self):

        pass

    def fail(self):
        print('failed')
        raise Exception

    def click(self, element):
        if element.is_displayed():
            print(element.location)

            element.click()
        else:
            self.click(element.parent)

    ###################
    # Element Getters
    ###################

    def filt_els_by_text(self, b_class, b_text):
        # returns a list of elements of a certain class WITH specific text inside
        return [b for b in self.get_els_by_class(b_class) if b.text == b_text]

    def get_els_by_name(self, value):
        self.el_wait(By.NAME, value)
        return self.driver.find_elements_by_name(value)

    def get_els_by_class(self, value):
        self.el_wait(By.CLASS_NAME, value)
        return self.driver.find_elements_by_class_name(value)

    def el_wait(self, by, value):
        element_present = EC.presence_of_element_located((by, value))
        WebDriverWait(self.driver, self.timeout).until(element_present)

    ###########
    # Utility
    ###########

    def gen_html_file(self, text):
        with open('page.html', 'w') as f:
            f.write(text)
