import time
from bs4 import BeautifulSoup
import initheadless
import initdb
import query
from selenium.webdriver.support.ui import Select
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

db = initdb.get_db()
cursor = initdb.get_cursor(db)
# initdb.create_soal_rilis_db()

def log(text):
    print (text, file=open("log.txt", "a"))
    print (get_date(), file=open("log.txt", "a"))

def get_date():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt

# delete log
f = open("log.txt", "w").close()

def get_soal_rilis(url):
    try:
        browser = initheadless.headless_browser()
        browser.get(url)
        time.sleep(5)

        get_rilis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div/div")
        for rilis in get_rilis:
            soup_rilis = BeautifulSoup(rilis.get_attribute("innerHTML"), "lxml")
            link_rilis = soup_rilis.find_all("a")
            for link in link_rilis:
                data = []
                judul = link.text.lstrip().rstrip()
                if "2019" in judul:
                    tahun = "2019"

                data.append(tahun)
                data.append(link.get("href"))
                data.append(judul)

                print(data)
                query.soal_rilis(data)
        browser.quit()
    except Exception as ex:
        print(ex)
        browser.quit()

links = [
        "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!soal_release!01&01&0048!b&01&T&T&1&!1!&"
        ]

with ProcessPoolExecutor(max_workers=1) as executor:
    futures = [ executor.submit(get_soal_rilis, url) for url in links ]
    results = []
    for result in as_completed(futures):
        results.append(result)