import os
import socket
from urllib.parse import urlparse

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

import pytest


@tag('user')
@override_settings(ALLOWED_HOSTS=['*'])
class UserBaseTestCase(StaticLiveServerTestCase):
    fixtures = ['test_users']
    """
    Provides base test class which connects to the Docker
    container running selenium.
    """

    host = '0.0.0.0'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Set host to externally accessible web server address
        cls.host = socket.gethostbyname(socket.gethostname())

        host = "selenium-hub"

        # Chrome
        desired_capabilities = DesiredCapabilities.CHROME.copy()
        desired_capabilities['platform'] = 'Linux'
        desired_capabilities['browser_version'] = 89
        desired_capabilities['chrome_driver'] = 89

        # Firefox
        #desired_capabilities=DesiredCapabilities.FIREFOX.copy()

        cls.driver = webdriver.Remote(
            command_executor=f"http://{host}:4444/wd/hub",
            desired_capabilities=desired_capabilities
        )
        cls.driver.maximize_window()
        #cls.driver.implicitly_wait(5)

    def setUp(self):
        """
        As a test user with valid credentials, I should gain access to Qlma news page.
        """
        self.driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('testusername')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('testpassword')
        self.driver.find_element_by_xpath('//button[@type="submit" and text()="Login"]').click()

        path = urlparse(self.driver.current_url).path
        self.assertEqual('/news', path)

    def test_user_news_page_title(self):
        """
        As a test user, I navigate to News page.
        """
        self.driver.find_element_by_xpath('//*[@id="pageLinksRight"]/div/ul/li/a[contains(@href, "/news")]').click()
        body_text = self.driver.find_element_by_tag_name('body').text
        self.assertIn('News', body_text)

    def test_user_quicklinks_header(self):
        """
        As a test user, I should see QuickLinks header.
        """
        h3_text = self.driver.find_element_by_xpath('//*[@id="pageLinksRight"]/div/h3').text
        self.assertIn('Quick links', h3_text)

    def test_user_navigate_to_messages(self):
        """
        As a test user, I navigate to Messages page.
        """
        self.driver.find_element_by_xpath('//*[@id="pageLinksRight"]/div/ul/li/a[contains(@href, "/messages/")]').click()

        body_text = self.driver.find_element_by_tag_name('body').text
        self.assertIn('Latest messages', body_text)

        path = urlparse(self.driver.current_url).path
        self.assertEqual('/messages/', path)


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
