from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pickle

def start_and_load_cookies():
    options = Options()
    options.headless = True
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
    driver.get("https://www.twitter.com/")
    cookies = pickle.load(open("twittercookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    return driver