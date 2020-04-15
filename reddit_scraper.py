from bs4 import BeautifulSoup
from requests import get


class RedditScraper:

    def __init__(self):
        self.url = "https://old.reddit.com"

    def get_soup(self, subreddit=None):
        url = self.url if subreddit is None else self.url + "/r/" + subreddit
        res = get(url, headers={"User-agent": "Mozilla/5.0"})
        if res.status_code != 200:
            print("Request got status code {}".format(res.status_code))
            return
        # open("index.html", "w").write(res.text)
        return BeautifulSoup(res.text, "html.parser")

    def get_posts_from_soup(self, soup):
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


def main():
    scraper = RedditScraper()

    # Fetch the page from the korea subreddit
    soup = scraper.get_soup(subreddit="korea")
    posts = scraper.get_posts_from_soup(soup)

    for post in posts:
        print("'{}' by {}".format(post["title"], post["author"]))


main()
