import yarl
import logging
from pathlib import Path
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from typing import List

logger = logging.getLogger(__name__)
implemented_browsers = {"chrome", "firefox"}


class Browser:
    def __init__(self, browser="chrome", headless=False, extensions: List[str] = None, user_data_dir: str = None):
        assert browser in implemented_browsers
        if browser == "chrome":
            self.open_chrome(headless, extensions, user_data_dir=user_data_dir)
        elif browser == "firefox":
            logger.error("Firefox implementation not yet complete")
            # self.open_firefox()
        self.num_tabs = 1
        self.current_tab = 0

    def open_chrome(
        self,
        headless: bool = False,
        extensions: List[str] = None,
        proxy: str = None,
        user_data_dir: str = None,
    ):
        desired = DesiredCapabilities.CHROME
        options = Options()
        if extensions is not None:
            for extension in extensions:
                options.add_argument(f"--load-extension={extension}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("window-size=1920,1080")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        )
        options.add_argument("--log-level=3")
        options.add_argument(
            "--no-sandbox"
        )  # https://stackoverflow.com/a/50725918/1689770
        options.add_argument(
            "--disable-infobars"
        )  # https://stackoverflow.com/a/43840128/1689770
        options.add_argument(
            "--disable-dev-shm-usage"
        )  # https://stackoverflow.com/a/50725918/1689770
        options.add_argument(
            "--disable-browser-side-navigation"
        )  # https://stackoverflow.com/a/49123152/1689770
        if user_data_dir:
            user_data_dir = Path(user_data_dir).absolute()
            options.add_argument(f"--user-data-dir={user_data_dir}")
            logger.info(f"Storing user data in: {user_data_dir}")
        if headless:
            options.add_argument(
                "--disable-gpu"
            )  # https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc
            options.add_argument("--headless")
            logger.info("Running browser in headless mode")
        if proxy is not None:
            options.add_argument("--proxy-server={}".format(proxy))
        driver = webdriver.Chrome(
            executable_path=binary_path, options=options, desired_capabilities=desired
        )
        self.driver = driver

    def open_firefox(self, headless=False):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference("useAutomationExtension", False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX
        firefox_path = str(Path(__file__).parent / "bin/geckodriver.exe")
        return webdriver.Firefox(
            firefox_profile=profile,
            executable_path=firefox_path,
            desired_capabilities=desired,
        )

    def new_tab(self, name):
        self.driver.execute_script(f"window.open('about:blank', '{name}');")
        self.num_tabs = len(self.driver.window_handles)

    def navigate_to(self, url):
        self.driver.get(url)
        logger.info(f"Successful navigation to: {url}")

    def to_tab(self, tab):
        assert 0 <= tab and tab < self.num_tabs
        self.current_tab = tab
        self.driver.switch_to.window(self.driver.window_handles[tab])

    def close(self):
        self.driver.close()

    def refresh(self):
        self.driver.refresh()

    def already_loaded(self, url):
        current_url = yarl.URL(self.driver.current_url)
        return yarl.URL(url) == current_url


def already_loaded(driver, url):
    current_url = yarl.URL(driver.current_url)
    return yarl.URL(url) == current_url
