import pickle
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Chr_options
from selenium.common import exceptions

URL = "https://hordes.io"

class Driver:

    def __init__(self, driver_path: str = None):
        self.driver_path = driver_path
        self.driver = webdriver.Chrome
        self.chrome_options = Chr_options()
        self.chrome_options.add_argument('--start-maximized')
        self.chrome_options.add_experimental_option("w3c", False)

    def start(self):
        try:
            if self.driver_path:
                self.driver = self.driver(self.driver_path, chrome_options=self.chrome_options)
            else:
                self.driver = self.driver(chrome_options=self.chrome_options)

        except exceptions.WebDriverException:
            print('Could not initiate web driver...')
            exit(1)

        # Load cookies if exist
        if os.path.isfile("hordes_cookies.pkl"):
            self.driver.get('https://www.google.com/')  # redirect to this website before add cookies so that if we direct back to hordes.io then we will logged in.
            print("Adding cookies to browser...")
            for cookie in pickle.load(open("hordes_cookies.pkl", "rb")):
                self.driver.add_cookie(cookie)

        self.driver.get(URL)

    def quit(self):
        """
        Save cookies from session and destroy driver
        """
        print("Saving cookies...")
        pickle.dump(self.driver.get_cookies(), open("hordes_cookies.pkl", "wb"))
        self.driver.close()
        print("Quitting driver...")
        self.driver.quit()
        exit()