import util.package_constants as const

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#############
# Constants
#############

driver = None
timeout = const.timeout

by_types = [
    'ID',
    'NAME',
    'XPATH',
    'LINK_TEXT',
    'PARTIAL_LINK_TEXT',
    'TAG_NAME',
    'CLASS_NAME',
    'CSS_SELECTOR',
]

###########
# Setup
###########


def generate_driver():
    global driver
    driver = webdriver.Chrome()


def set_driver(web_driver):
    global driver
    driver = web_driver

###################
# Element Getters
###################


def filt_els_by_text(by, value, text):
    # returns a list of elements of a certain class WITH specific text inside
    return [e for e in get_els_by(by, value) if e.text == text]


def get_el_by(by, value):
    if by is by_types[0]:
        el_wait(By.ID, value)
        return driver.find_element_by_id(value)

    if by is by_types[1]:
        el_wait(By.NAME, value)
        return driver.find_element_by_name(value)

    elif by is by_types[2]:
        el_wait(By.XPATH, value)
        return driver.find_element_by_xpath(value)

    elif by is by_types[3]:
        el_wait(By.LINK_TEXT, value)
        return driver.find_element_by_link_text(value)

    elif by is by_types[4]:
        el_wait(By.PARTIAL_LINK_TEXT, value)
        return driver.find_element_by_partial_link_text(value)

    elif by is by_types[5]:
        el_wait(By.TAG_NAME, value)
        return driver.find_element_by_tag_name(value)

    elif by is by_types[6]:
        el_wait(By.CLASS_NAME, value)
        return driver.find_element_by_class_name(value)

    elif by is by_types[7]:
        el_wait(By.CSS_SELECTOR, value)
        return driver.find_element_by_css_selector(value)


def get_els_by(by, value):
    if by is by_types[1]:
        el_wait(By.NAME, value)
        return driver.find_elements_by_name(value)

    elif by is by_types[2]:
        el_wait(By.XPATH, value)
        return driver.find_elements_by_xpath(value)

    elif by is by_types[3]:
        el_wait(By.LINK_TEXT, value)
        return driver.find_elements_by_link_text(value)

    elif by is by_types[4]:
        el_wait(By.PARTIAL_LINK_TEXT, value)
        return driver.find_elements_by_partial_link_text(value)

    elif by is by_types[5]:
        el_wait(By.TAG_NAME, value)
        return driver.find_elements_by_tag_name(value)

    elif by is by_types[6]:
        el_wait(By.CLASS_NAME, value)
        return driver.find_elements_by_class_name(value)

    elif by is by_types[7]:
        el_wait(By.CSS_SELECTOR, value)
        return driver.find_elements_by_css_selector(value)


def el_wait(by, value):
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
