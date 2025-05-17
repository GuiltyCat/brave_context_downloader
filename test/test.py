from unittest import TestCase

from brave_context_downloader import Downloader, Cookie, UserAgent


class TestCookie(TestCase):
    def test_get_cookie(self):
        cookie = Cookie()
        cookies = cookie.get_cookie()
        self.assertIsInstance(cookies, dict)
        print(cookies)


class TestUserAgent(TestCase):
    def test_get_user_agent(self):
        ua = UserAgent()
        user_agent = ua.get_user_agent()
        self.assertIsInstance(user_agent, str)
        print(user_agent)


class TestDownloader(TestCase):
    def test_get_html(self):
        dl = Downloader("Mozilla/5.0", {}, 1)
        html = dl.get_html("http://example.com")
        self.assertIsInstance(html, str)
        print(html)
