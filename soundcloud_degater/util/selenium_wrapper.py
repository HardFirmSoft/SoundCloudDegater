from selenium import webdriver
from selenium.webdriver.chrome.options import Options


###########
# Setup
###########


def new_driver():
    """If you want to generate a new web_driver for some reason."""

    chrome_options = Options()
   # chrome doesn't allow downloading in headless mode :(
   # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def allow_downloads(driver, download_dir):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)

###################
# Element Getters
###################


# def filt_els_by_text(driver, by, value, text):
#     # returns a list of elements of a certain class WITH specific text inside
#     return [e for e in get_elements_with_wait(driver, by, value) if e.text == text]


# def get_element_with_wait(driver, by, value):
#     switch = {
#         'ID': [By.ID, driver.find_element_by_id],
#         'NAME': [By.NAME, driver.find_element_by_name],
#         'XPATH': [By.XPATH, driver.find_element_by_xpath],
#         'LINK_TEXT': [By.LINK_TEXT, driver.find_element_by_link_text],
#         'PARTIAL_LINK_TEXT': [By.PARTIAL_LINK_TEXT, driver.find_element_by_partial_link_text],
#         'TAG_NAME': [By.TAG_NAME, driver.find_element_by_tag_name],
#         'CLASS_NAME': [By.CLASS_NAME, driver.find_element_by_class_name],
#         'CSS_SELECTOR': [By.CSS_SELECTOR, driver.find_element_by_css_selector],
#     }
#
#     el_wait(driver, switch[by][0], value)
#     return switch[by][1](value)


# def get_elements_with_wait(driver, by, value):
#     switch = {
#         'ID': [By.ID, driver.find_elements_by_id],
#         'NAME': [By.NAME, driver.find_elements_by_name],
#         'XPATH': [By.XPATH, driver.find_elements_by_xpath],
#         'LINK_TEXT': [By.LINK_TEXT, driver.find_elements_by_link_text],
#         'PARTIAL_LINK_TEXT': [By.PARTIAL_LINK_TEXT, driver.find_elements_by_partial_link_text],
#         'TAG_NAME': [By.TAG_NAME, driver.find_elements_by_tag_name],
#         'CLASS_NAME': [By.CLASS_NAME, driver.find_elements_by_class_name],
#         'CSS_SELECTOR': [By.CSS_SELECTOR, driver.find_elements_by_css_selector],
#     }
#
#     el_wait(driver, switch[by][0], value)
#     return switch[by][1](value)


# def el_wait(driver, by, value, max_retry=5, retry_backoff=5):
#     """Wait until an element appears with retry"""
#     i = 0
#     time_waited = 0
#     while i < max_retry:
#         try:
#             element_present = EC.presence_of_element_located((by, value))
#             WebDriverWait(driver, const.timeout).until(element_present)
#             return
#         except TimeoutException:
#             i += 1
#             time_waited += const.timeout + retry_backoff
#             print(f"Retrying find of {value} in {retry_backoff} seconds...")
#             time.sleep(retry_backoff)
#     raise TimeoutException(f"Timed out after {time_waited} seconds.")
################
# Interactions
################


def get(driver, url):
    driver.get(url)


# def click(element):
#     if element.is_displayed():
#         element.click()
#     else:
#         click(element.parent)
