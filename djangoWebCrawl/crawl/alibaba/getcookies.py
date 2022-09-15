from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def webdriver_settings():
    chrome_debug_port = 9999
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{chrome_debug_port}")
    browser = webdriver.Chrome(options=chrome_options)

    browser.set_page_load_timeout(35)
    browser.set_script_timeout(35)
    return browser


def get_new_cookies():
    browser = webdriver_settings()

    while True:
        time.sleep(2)
        browser.get('https://www.1688.com/')
        try:
            browser.find_element_by_xpath('//*[@id="alibar"]/div[1]/div[2]/ul/li[3]/a').click()
            browser.find_element_by_xpath('//input[@name="fm-login-id"]').send_keys('your Taobao Username')
            browser.find_element_by_xpath('//input[@name="fm-login-password"]').send_keys('Your Taobao Password')
            browser.find_element_by_xpath('//button[@type="submit"]').click()
        except:
            break

    _m_h5_tk_cookies = browser.get_cookie('_m_h5_tk')['value']
    _m_h5_tk_enc_cookies = browser.get_cookie('_m_h5_tk_enc')['value']
    return _m_h5_tk_cookies, _m_h5_tk_enc_cookies