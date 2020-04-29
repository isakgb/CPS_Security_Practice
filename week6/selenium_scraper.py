from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from bs4 import BeautifulSoup
from time import sleep


def get_posts_from_soup(soup):
    # Find the divs containing posts
    post_divs = []

    for div in soup.find_all("div"):
        if "class" in div.attrs and "thing" in div.attrs["class"]:
            post_divs.append(div)

    posts = []

    for div in post_divs:
        user_op = div.attrs["data-author"]
        a_elements = div.find_all("a")
        for a in a_elements:
            if "class" in a.attrs and "title" in a.attrs["class"]:
                posts.append({"title": a.string, "author": user_op})
                continue

    return posts


def get_userpost(driver: WebDriver, url):
    driver.get(url)
    sleep(2)
    paragraphs = driver.find_elements_by_xpath("/html/body/div[4]/div[1]/div[1]/div[2]/div[2]/form/div/div/p")

    return "\n\n".join([p.text for p in paragraphs])


driver = webdriver.Chrome("chromedriver.exe")


sleep(3)


try:
    driver.get("https://old.reddit.com")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    print("Front page posts:")
    [print(post) for post in get_posts_from_soup(soup)]

    search_element = driver.find_element_by_name("q") # The search box
    search_element.send_keys("chung ang university\n") # Newline makes it search

    print("Posts related to Chung-Ang University")

    sleep(3)

    urls = []

    for search_result in driver.find_elements_by_class_name("search-result"):
        a = search_result.find_element_by_tag_name("a")
        url = a.get_attribute("href")
        urls.append(url)
    for url in urls:
        print("Attempting to read post {}".format(url))
        print(get_userpost(driver, url))
        sleep(3)

finally:
    sleep(1)
    driver.quit()