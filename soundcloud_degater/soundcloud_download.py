from typing import List, Dict

from selenium import webdriver

import package_constants as const
from exceptions import SoundCloudDegaterException


class SoundCloudDownloader(object):
    """Static class for all SoundCloud downloading functionality."""
    driver = webdriver.Chrome()

    @classmethod
    def _get_webpage(cls, url: str):
        """Change the current webpage to the URL"""
        cls.driver.get(url)

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
        download_elements = cls.driver.find_elements_by_class_name(const.link_option_class)
        for element in download_elements:
            if element.text == const.free_download:
                element.click()
                # Break cause Selenium tries to load elements that don't exist anymore
                break
