import time
import os

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchWindowException

import soundcloud_degater.util.selenium_wrapper as sw


class FanlinkParser(object):
    def __init__(self, driver, fb_email: str, fb_password: str, download_dir):
        self._driver = driver
        self._download_dir = download_dir
        self._fb_password = fb_password
        self._email = fb_email
        self._downloaded_songs = []
        self._followed_artists_urls = []
        self._steps = [
            self._home,
            self._single_download,
            self._follow_sc,
            self._click_facebook_button,
            self._sign_in_and_authorize,
            self._download,
        ]

    def parse(self, url, retries=50, backoff=0.5):
        print(f"Sending HTTP GET request to: {url}...")
        sw.get(self._driver, url)
        # Invoke list of functions.
        i = 1
        for step in self._steps:
            print(f"Executing step: {i} of {len(self._steps)}...")
            for j in range(1, retries):
                try:
                    step()
                    break
                except Exception:
                    print(f"Retrying step in {backoff} seconds")
                    time.sleep(backoff)
                    if j == retries-1:
                        raise
            i += 1

    ########################
    # Sequential Traversal
    ########################

    def _home(self):
        # click 'free download' (one of many options)
        buttons = [e for e in self._driver.find_elements_by_class_name('link-option-row-action')
                   if e.text == 'FREE DOWNLOAD']
        if buttons:
            buttons[0].click()
        else:
            raise Exception

    def _single_download(self):
        # click 'free download' (only option)
        buttons = [e for e in self._driver.find_elements_by_class_name('post-gate-btn')
                   if e.text == 'FREE DOWNLOAD']
        if buttons:
            buttons[0].click()
        else:
            raise Exception

    def _follow_sc(self):
        # click 'follow on soundcloud'
        buttons = [e for e in self._driver.find_elements_by_class_name('soundcloud')
                   if e.text == 'FOLLOW ON SOUNDCLOUD']
        if buttons:
            buttons[0].click()
        else:
            raise Exception

    def _click_facebook_button(self):
        # in new window, click on FB signin
        self._driver.switch_to_window(self._driver.window_handles[1])
        social_button = self._driver.find_element_by_partial_link_text('Sign in with Facebook')
        if social_button:
            social_button.click()

    def _sign_in_and_authorize(self):
        print('Signing in to Facebook...')
        email_box = self._driver.find_element_by_xpath("//*[@id='email']")
        email_box.send_keys(self._email)
        password_box = self._driver.find_element_by_xpath("//*[@id='pass']")
        password_box.send_keys(self._fb_password)
        password_box.send_keys(Keys.RETURN)

        # If the person has already authorized Soundcloud in Facebook, the window closes
        # Hack to implement a wait / retry
        import time
        for i in range(5, 1):
            try:
                if not len(self._driver.window_handles) == 1:
                    print("Authorizing SoundCloud on Facebook")
                    continue_button = self._driver.find_element_by_xpath("//*[@id='u_0_4']/div[2]/div[1]/div[1]/button")
                    continue_button.click()
                if not len(self._driver.window_handles) == 1:
                    print("Authorizing ToneDen on SoundCloud")
                    accept_toneden = self._driver.find_element_by_xpath("//*[@id='signup_authorize']")
                    accept_toneden.click()
            except NoSuchWindowException:
                time.sleep(1)
                print(f"Retrying in...{i}")

        self._driver.switch_to_window(self._driver.window_handles[0])

    def _download(self):
        number_of_files_before = len(os.listdir(self._download_dir))
        print("Downloading track...")
        sw.allow_downloads(self._driver, self._download_dir)
        element = self._driver.find_element_by_xpath(
            "//*[@id='app-component']/span/div[1]/div/div/div/div[3]/div/div/div/div[2]/div/span/a")
        element.click()
