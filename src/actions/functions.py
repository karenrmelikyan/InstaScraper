import time
import random

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def scrape_followers(browser, account) -> []:
    try:
        # Load user account page
        browser.get("https://www.instagram.com/{0}/".format(account))

        # Click 'followers' link
        wait_element_by_xpath(browser,
                              '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()

        # get follower popup window elem
        wait_element_by_class_name(browser, 'PZuss')
        timeout = 5
        while True:

            browser.execute_script('document.querySelector(".isgrP")'
                                   '.scrollTo({ top: document.querySelector(".isgrP").scrollHeight, behavior: '
                                   '"smooth" });')

            wait_element_by_class_name(browser, 'FPmhX')
            count = len(browser.find_elements_by_class_name('FPmhX'))
            newCount = count
            end_time = time.time() + timeout

            while True:
                wait_element_by_class_name(browser, 'FPmhX')
                newCount = len(browser.find_elements_by_class_name('FPmhX'))
                if newCount > count:
                    break
                time.sleep(0.5)
                if time.time() > end_time:
                    break

            if newCount == count:
                break
        wait_element_by_class_name(browser, 'FPmhX')
        followers = browser.find_elements_by_class_name('FPmhX')

        output = []
        for i in range(0, len(followers)):
            output.append(followers[i].text)

        return output

    except Exception as ex:
        print(ex)
        wait_element_by_class_name(browser, 'FPmhX')
        followers = browser.find_elements_by_class_name('FPmhX')

        output = []
        for i in range(0, len(followers)):
            output.append(followers[i].text)

        return output


def get_posts_by_hashtag(browser, hashtag, scroll_count=None) -> []:
    posts_urls = []
    posts_count = 0
    count = 0

    browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')

    # collect data and return count for
    # compare with previous result
    def get_data_by_scroll() -> int:
        for item in range(0, 3):
            time.sleep(0.5)
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        wait_element_by_tag_name(browser, 'a')
        href = browser.find_elements_by_tag_name('a')

        for item in href:
            href = item.get_attribute('href')
            if '/p/' in href:
                posts_urls.append(href)

        return len(posts_urls)

    # manage loops
    if scroll_count:
        for i in range(0, scroll_count):
            get_data_by_scroll()
    else:
        while True:
            count = get_data_by_scroll()
            if posts_count == count:
                break
            else:
                posts_count = count

    return posts_urls


def like_post(browser, post_url) -> None:
    try:
        browser.get(post_url)
        wait_element_by_xpath(browser,
                              '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span['
                              '1]/button').click()
    except Exception as ex:
        print(ex)
        print('The problem with put_like function')
        browser.close()
        browser.quit()


def like_many_posts_of_user(browser, user_url, post_count) -> None:
    try:
        browser.get(user_url)

        # get posts count of user
        posts_count = wait_element_by_xpath(browser,
                                            '//*[@id="react-root"]/section/main/div/header/section/ul/li['
                                            '1]/span').text
        posts_count = int(posts_count.replace('posts', ''))

        # get count for scrolling
        scroll_count = int(posts_count / 12)

        # get urls per scrolled page
        post_urls = []
        for i in range(1, scroll_count):
            refs = browser.find_elements_by_tag_name('a')

            # filtration urls by post
            for item in refs:
                url = item.get_attribute('href')
                if '/p/' in url:
                    post_urls.append(url)
                    print(url)

        # scrolling
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        # filtration extra urls
        post_urls = list(set(post_urls))

        # to put likes to defined amount of posts
        for post_url in post_urls[0:post_count]:
            like_post(browser, post_url)
            time.sleep(random.randrange(2, 4))

    except Exception as ex:
        print(ex)
        print('Exception in like_many_posts_of_user function')


def wait_element_by_tag_name(browser, tag_name):
    return WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located((By.TAG_NAME, tag_name)))


def wait_element_by_class_name(browser, class_name):
    return WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located((By.CLASS_NAME, class_name)))


def wait_element_by_xpath(browser, element_xpath):
    return WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located((By.XPATH, element_xpath)))
