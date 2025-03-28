import os
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from dotenv import load_dotenv
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.remote.webelement import WebElement
from utils import get_connected_device
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

class TestAppium(unittest.TestCase):
    appium_server_url = 'http://127.0.0.1:4723/wd/hub'
    driver: WebDriver
    view_waiter: WebDriverWait

    def setUp(self):
        load_dotenv()
        platform, uuid = get_connected_device()
        if platform == "Android":
            self.driver = self.setup_android_driver()
            self.view_waiter = WebDriverWait(self.driver, 7)
        elif platform == "iOS":
            self.driver = self.setup_ios_driver(ios_uuid=uuid)
            self.view_waiter = WebDriverWait(self.driver, 7)
        else:
            print("Can't find connected device.")
            quit()

    # Android setup
    def setup_android_driver(self):
        print("Start Android Test")
        print(f"package name: {os.getenv('ANDROID_APP_PACKAGE_NAME')}")
        print(f"appActivity name: {os.getenv('APP_ACTIVITY_FOR_ANDROID')}")

        capabilities = dict(
            platformName="Android",
            automationName="uiautomator2",
            deviceName="Android",
            appPackage=os.getenv('ANDROID_APP_PACKAGE_NAME'),
            appActivity=os.getenv("APP_ACTIVITY_FOR_ANDROID"),
            noReset="true"
        )

        return webdriver.Remote(self.appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    # iOS setup
    def setup_ios_driver(self, ios_uuid):
        print("Start iOS Test")

        capabilities = dict(
            platformName="iOS",
            platformVersion=os.getenv("IOS_PLATFORM_VERSION"),
            deviceName='iPhone 15 Pro Max',
            app=os.getenv('IOS_APP_PACKAGE_NAME'),
            automationName='XCUITest',
            xcodeOrgId=os.getenv('IOS_DEVELOPER_ID'),
            xcodeSigningId='Apple Development',
            udid=ios_uuid,
        )

        return webdriver.Remote(self.appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tear_down(self) -> None:
        if self.driver:
            self.driver.quit()

    def wait_for_view(self, view_id=None, view_xpath=None):
        """ wait for certain view """
        if view_id:
            self.view_waiter.until(EC.visibility_of_element_located((AppiumBy.ID, view_id)))
        else:
            self.view_waiter.until(EC.visibility_of_element_located((AppiumBy.XPATH, view_xpath)))

    def is_scrollable(self):
        try:
            scrollable_element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                          'new UiSelector().scrollable(true)')
            scrollable_state = scrollable_element.get_attribute("scrollable")
            return scrollable_state == "true"
        except Exception as e:
            return False

    def updown_scroll_screen(self):
        """scroll the display using TouchAction"""
        # get current display size
        screen_size = self.driver.get_window_size()
        width = screen_size['width']
        height = screen_size['height']

        # get center coordinates
        center_x = width // 2
        center_y = height // 2

        # scroll end point (to down)
        end_y = int(height * 0.2)

        # do W3C action
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(center_x, center_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.5)
        actions.w3c_actions.pointer_action.move_to_location(center_x, end_y)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()

    def scroll_to_element(self, view_id=None, view_xpath=None, max_attempts=4) -> WebElement:
        """try to find element with scrolling"""
        attempts = 0

        while attempts < max_attempts:
            try:
                if view_id:
                    element = self.driver.find_element(AppiumBy.ID, view_xpath)
                else:
                    element = self.driver.find_element(AppiumBy.XPATH, view_xpath)

                if element.is_displayed():
                    return element
            except Exception as e:
                # if it fails to find element, scroll again.
                self.updown_scroll_screen()
            attempts += 1
        raise Exception(f"Unable to find the element with identifier {view_id or view_xpath} after {max_attempts} attempts.")

    def get_view(self, view_id=None, view_xpath=None) -> WebElement:
        """
        wait for certain view and return it for next action
        1. wait for it until 7 seconds.
            * find scroll element and scroll it for 4 times unit find it.
        2. if it finds element, return it
            * if it can't find element, raise exception.
        """
        if view_id:
            # ex) view_id=example_text_view
            try:
                self.view_waiter.until(EC.visibility_of_element_located((AppiumBy.ID, view_id)))
                return self.driver.find_element(AppiumBy.ID, view_id)
            except Exception as e:
                return self.scroll_to_element(view_id=view_id)

        else:
            # ex) Android: view_xpath="//*[@text="text_name"]"  iOS: "//*[@name="text_name"]"
            try:
                self.view_waiter.until(EC.visibility_of_element_located((AppiumBy.XPATH, view_xpath)))
                return self.driver.find_element(AppiumBy.XPATH, view_xpath)
            except Exception as e:
                return self.scroll_to_element(view_xpath=view_xpath)


    def test_start(self):
        # App test visualize
        print("not yet here")
