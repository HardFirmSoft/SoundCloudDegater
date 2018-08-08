from typing import List, Dict

import package_constants as const
from exceptions import SoundCloudDegaterException


from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of


class SoundCloudDownloader(object):
    """Static class for all SoundCloud downloading functionality."""
    browser = webdriver.Chrome()

    @classmethod
    def _get_webpage(cls, url: str):
        """Change the current webpage to the URL"""
        cls.browser.get(url)

    @staticmethod
    def _categorize_purchase_link(url: str) -> str:
        """Determine what the purchase site is, and if we can handle it."""
        check = [site for site in const.handled_sites if site in url]
        if check:
            return check[0]
        else:
            raise SoundCloudDegaterException(f"Url {url} is not in our list of recognised domains!")

    @classmethod
    def download_tracks(cls, tracks: List[Dict]):
        for track in tracks:
            try:
                link_type = cls._categorize_purchase_link(track['purchase_url'])
                SoundCloudDownloader._download_track(link_type, track)
            except SoundCloudDegaterException as e:
                const.logger.warn(str(e))
                continue

    @classmethod
    def _download_track(cls, link_type: str, track: dict):
        # to do
        # actually DOWNLOAD track

        const.logger.info(f"Downloading track: {track['title']} from {track['purchase_url']}...")
        if link_type == const.fanlink:
            cls._download_from_fanlink(track['purchase_url'])

    @classmethod
    def _download_from_fanlink(cls, url: str):
        # Currently is able to navigate to download page and find the free download button
        cls._get_webpage(url)

        # first layer
        print('\nfirst layer')

        print(cls.browser.current_url)
        download_elements = cls.browser.find_elements_by_class_name(const.FL_first_button_class)
        for element in download_elements:
            if element.text == 'FREE DOWNLOAD':
                print(element)
                element.click()
                # Break cause Selenium tries to load elements that don't exist anymore
                break

        with cls.wait_for_page_load(timeout=10):
            # second layer
            print('\nsecond layer')
            print(cls.browser.current_url)

            download_elements = cls.browser.find_elements_by_link_text('Free Download')
            for element in download_elements:
                print(element)
                element.click()
                # Break cause Selenium tries to load elements that don't exist anymore
                break

    # def _download

    ###########
    # Utility
    ###########

    @contextmanager
    def wait_for_page_load(cls, timeout=30):
        old_page = cls.browser.find_element_by_tag_name('html')
        yield
        WebDriverWait(cls.browser, timeout).until(
            staleness_of(old_page)
        )
