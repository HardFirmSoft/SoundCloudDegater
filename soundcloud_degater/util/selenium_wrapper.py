from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import soundcloud_degater.util.package_constants as const

#############
# Constants
#############

driver = webdriver.Chrome()
timeout = const.timeout



###########
# Setup
###########


def get_driver():
    """Refers to the static driver in this file."""
    return driver


def new_driver():
    """If you want to generate a new web_driver for some reason."""
    return webdriver.Chrome()

###################
# Element Getters
###################


def filt_els_by_text(by, value, text):
    # returns a list of elements of a certain class WITH specific text inside
    return [e for e in get_elements_with_wait(by, value) if e.text == text]


def get_element_with_wait(by, value):
    switch = {
        'ID': [By.ID, driver.find_element_by_id],
        'NAME': [By.NAME, driver.find_element_by_name],
        'XPATH': [By.XPATH, driver.find_element_by_xpath],
        'LINK_TEXT': [By.LINK_TEXT, driver.find_element_by_link_text],
        'PARTIAL_LINK_TEXT': [By.PARTIAL_LINK_TEXT, driver.find_element_by_partial_link_text],
        'TAG_NAME': [By.TAG_NAME, driver.find_element_by_tag_name],
        'CLASS_NAME': [By.TAG_NAME, driver.find_element_by_class_name],
        'CSS_SELECTOR': [By.CSS_SELECTOR, driver.find_element_by_css_selector],
    }

    el_wait(switch[by][0], value)
    return switch[by][1](value)


def get_elements_with_wait(by, value):
    switch = {
        'ID': [By.ID, driver.find_elements_by_id],
        'NAME': [By.NAME, driver.find_elements_by_name],
        'XPATH': [By.XPATH, driver.find_elements_by_xpath],
        'LINK_TEXT': [By.LINK_TEXT, driver.find_elements_by_link_text],
        'PARTIAL_LINK_TEXT': [By.PARTIAL_LINK_TEXT, driver.find_elements_by_partial_link_text],
        'TAG_NAME': [By.TAG_NAME, driver.find_elements_by_tag_name],
        'CLASS_NAME': [By.TAG_NAME, driver.find_elements_by_class_name],
        'CSS_SELECTOR': [By.CSS_SELECTOR, driver.find_elements_by_css_selector],
    }

    el_wait(switch[by][0], value)
    return switch[by][1](value)


def el_wait(by, value):
    """Wait until an element appears"""
    element_present = EC.presence_of_element_located((by, value))
    WebDriverWait(driver, timeout).until(element_present)


################
# Interactions
################

def get(url):
    driver.get(url)


def click(element):
    if element.is_displayed():
        print(element.location)

        element.click()
    else:
        click(element.parent)
