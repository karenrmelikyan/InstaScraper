from selenium.webdriver.common.keys import Keys
from src.auth.config import *
from src.actions.functions import *
import time
import json


def authentication(browser) -> bool:
    # TO TRY LOGIN VIA SAVED EARLIER COOKIES
    try:
        # in first going to the login page
        browser.get('https://www.instagram.com/accounts/login/')

        # waiting for login form loading
        wait_element_by_xpath(browser, '//*[@id="loginForm"]/div/div[3]')

        # add exist cookies for authentication
        add_cookies(browser)

        # going to the Home page for login success checking
        browser.get('https://www.instagram.com/')

        # if login by cookies was successful
        # click 'Not Now'(notification) button
        wait_element_by_xpath(browser, '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    except Exception as ex:
        # IF COOKIES WERE EXPIRED,
        # TO PRODUCED LOGIN PROCESS
        if is_login_page(browser):
            login_status = login(username, password, browser)
            save_new_cookies(browser)
            return login_status

        print(ex)
        print('Exception in authentication function: cookies was expired and probably also, not happened '
              'redirecting to login page')
        return False

    return True


def login(username, password, browser) -> bool:
    try:
        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(1)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(1)

        # push 'Log In'
        password_input.send_keys(Keys.ENTER)

        # push 'Save info'
        wait_element_by_xpath(browser,
                                       '//*[@id="react-root"]/section/main/div/div/div/section/div/button').click()

        # push 'Not Now' (notification)
        wait_element_by_xpath(browser,
                                       '/html/body/div[4]/div/div/div/div[3]/button[2]').click()

    except Exception as ex:
        print(ex)
        print('Exception in "login" function')
        return False

    return True


def add_cookies(browser) -> bool:
    try:
        with open('src/auth/cookies', 'r') as file:
            cookies = json.loads(file.read(1500))
        for cookie in cookies:
            browser.add_cookie(cookie)
    except Exception as ex:
        print(ex)
        print('Exception in add_cookies function')
        return False

    return True


def save_new_cookies(browser) -> bool:
    try:
        cookies = browser.get_cookies()
        with open('src/auth/cookies', 'w') as file:
            file.write(json.dumps(cookies))
    except Exception as ex:
        print(ex)
        return False

    return True


def is_login_page(browser) -> bool:
    try:
        browser.find_element_by_name('username')
        browser.find_element_by_name('password')
    except Exception as ex:
        return False

    return True
