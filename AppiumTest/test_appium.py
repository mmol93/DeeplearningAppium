import os
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from dotenv import load_dotenv
from utils import get_connected_device
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy


class TestAppium(unittest.TestCase):
    appium_server_url = 'http://127.0.0.1:4723/wd/hub'
    driver: WebDriver

    def setUp(self):
        load_dotenv()
        platform, uuid = get_connected_device()
        if platform == "Android":
            self.driver = self.setup_android_driver()
        elif platform == "iOS":
            self.driver = self.setup_ios_driver(ios_uuid=uuid)
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

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_start(self):
        # App test visualize
        self.driver.activate_app(os.getenv('ANDROID_APP_PACKAGE_NAME'))

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((AppiumBy.ID, 'login_viewpager')))
        self.driver.find_element(AppiumBy.ID, 'login_fragment_reg_button').click()
