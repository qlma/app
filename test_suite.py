import socket
from urllib.parse import urlparse

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

import pytest


@tag('admin')
@override_settings(ALLOWED_HOSTS=['*'])
class AdminBaseTestCase(StaticLiveServerTestCase):
    fixtures = ['admin_user']
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

        cls.driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )

        cls.driver.implicitly_wait(5)

    def setUp(self):
        """
        As a superuser with valid credentials, I should gain access to the Django admin.
        """
        self.driver.get('%s%s' % (self.live_server_url, '/admin/'))
        username_input = self.driver.find_element_by_name('username')
        username_input.send_keys('admin')
        password_input = self.driver.find_element_by_name('password')
        password_input.send_keys('admin')
        self.driver.find_element_by_xpath('//input[@value="Log in"]').click()

        path = urlparse(self.driver.current_url).path
        self.assertEqual('/admin/', path)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

class AdminTestCase(AdminBaseTestCase):
    def test_admin_name(self):
        body_text = self.driver.find_element_by_tag_name('body').text
        self.assertIn('WELCOME, BOSS.', body_text) 




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

        cls.driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )

        cls.driver.implicitly_wait(5)

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

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


class UserTestCase(UserBaseTestCase):
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






