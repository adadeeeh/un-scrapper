from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

def headless_browser():
    options = Options()
    # local
    options.headless = False
    # browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    browser = webdriver.Firefox(options=options, executable_path="/home/pedro/Documents/selenium/geckodriver")
    # deploy
    # options.headless = True
    # browser = webdriver.Chrome(options=options)
    return browser