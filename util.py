import time
from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
os.environ['WDM_LOCAL'] = '1'

def retry_action(max_retries=3, wait_interval=1):
    """Decorator to retry a selenium action."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    print(f"[Retry {attempt}/{max_retries}] Error in {func.__name__}: {e}")
                    time.sleep(wait_interval)
            raise Exception(f"{func.__name__} failed after {max_retries} retries.")
        return wrapper
    return decorator


class SeleniumActions:
    def __init__(self, driver=None, retries=3, wait_interval=1):
        # self.driver = driver or webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.retries = retries
        # driver_path = ChromeDriverManager(path=".wdm").install()

        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--force-device-scale-factor=1")
        chrome_options.add_argument("--high-dpi-support=1")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Use cached driver path
        self.driver =webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def _get_retry_decorator(self):
        return retry_action(max_retries=self.retries, wait_interval=self.wait_interval)

    def open_url(self, url):
        self.driver.get(url)
        return self

    @retry_action()
    def click(self, xpath):
        self.driver.find_element(By.XPATH, xpath).click()
        return self

    @retry_action()
    def enter_text(self, xpath, text):
        element = self.driver.find_element(By.XPATH, xpath)
        element.clear()
        element.send_keys(text)
        return self

    @retry_action()
    def press_enter(self, xpath):
        self.driver.find_element(By.XPATH, xpath).send_keys(Keys.RETURN)
        return self

    @retry_action()
    def wait_for_element(self, xpath, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return self

    @retry_action()
    def hover(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        ActionChains(self.driver).move_to_element(element).perform()
        return self

    @retry_action()
    def scroll_to_element(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return self

    @retry_action()
    def switch_to_iframe(self, xpath):
        iframe = self.driver.find_element(By.XPATH, xpath)
        self.driver.switch_to.frame(iframe)
        return self

    @retry_action()
    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
        return self

    @retry_action()
    def get_text(self, xpath):
        return self.driver.find_element(By.XPATH, xpath).text

    @retry_action()
    def get_attribute(self, xpath, attribute_name):
        return self.driver.find_element(By.XPATH, xpath).get_attribute(attribute_name)

    @retry_action()
    def is_element_visible(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        return element.is_displayed()

    @retry_action()
    def element_exists(self, xpath):
        return len(self.driver.find_elements(By.XPATH, xpath)) > 0

    @retry_action()
    def fill_and_submit(self, xpath, text):
        element = self.driver.find_element(By.XPATH, xpath)
        element.clear()
        element.send_keys(text)
        element.send_keys(Keys.RETURN)
        return self

    def close_browser(self):
        self.driver.quit()
