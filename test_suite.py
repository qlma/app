import socket
from urllib.parse import urlparse

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

import pytest

@tag('selenium')
@override_settings(ALLOWED_HOSTS=['*'])
class BaseTestCase(StaticLiveServerTestCase):
    """
    Provides base test class which connects to the Docker
    container running selenium.
    """

    fixtures = ['admin_user', 'test_users']

    host = '0.0.0.0'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        
        # Set host to externally accessible web server address
        cls.host = socket.gethostbyname(socket.gethostname())

        cls.selenium = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )

        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_admin_login(self):
        """
        As a superuser with valid credentials, I should gain access to the Django admin.
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        path = urlparse(self.selenium.current_url).path
        self.assertEqual('/admin/', path)

        body_text = self.selenium.find_element_by_tag_name('body').text
        self.assertIn('WELCOME, BOSS.', body_text)


    def test_user_login(self):
        """
        As a test user with valid credentials, I should gain access to Qlma news page.
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('testusername')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('testpassword')
        self.selenium.find_element_by_xpath('//button[@type="submit" and text()="Login"]').click()

        path = urlparse(self.selenium.current_url).path
        self.assertEqual('/news', path)

        body_text = self.selenium.find_element_by_tag_name('body').text
        self.assertIn('News', body_text)

    def test_user_navigate_to_messages(self):
        self.test_user_login()
        """
        As a test user, I navigate to Messages page.
        """
        h3_text = self.selenium.find_element_by_xpath('//*[@id="pageLinksRight"]/div/h3').text
        self.assertIn('Quick links', h3_text)

        self.selenium.find_element_by_xpath('//*[@id="pageLinksRight"]/div/ul/li/a[contains(@href, "/messages/")]').click()

        body_text = self.selenium.find_element_by_tag_name('body').text
        self.assertIn('Latest messages', body_text)

        path = urlparse(self.selenium.current_url).path
        self.assertEqual('/messages/', path)
