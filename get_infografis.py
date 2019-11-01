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
# initdb.create_infografis_wilayah_db()

def log(text):
    print (text, file=open("log.txt", "a"))
    print (get_date(), file=open("log.txt", "a"))

def get_date():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt

# delete log
f = open("log.txt", "w").close()

def get_infografis_wilayah(url):
    try:
        browser = initheadless.headless_browser()
        browser.get(url)
        time.sleep(5)
        
        get_title = BeautifulSoup(browser.find_element_by_id("title").get_attribute("innerHTML"), "lxml").get_text()
        if "2019" in get_title:
            tahun = "2019"
        elif "2018" in get_title:
            tahun = "2018"

        get_jenjang = Select(browser.find_element_by_id("page"))
        jenjang = get_jenjang.first_selected_option.text

        if jenjang == "SMP/MTs" or jenjang == "SMA/MA":
            get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[1]/div/div[2]/input")
            for i in range(0, 2):
                if i == 0 and jenjang == "SMP/MTs":
                    jenis = "SMP"
                elif i == 1 and jenjang == "SMP/MTs":
                    jenis = "MTs"
                elif i == 0 and jenjang == "SMA/MA":
                    jenis = "SMA"
                else:
                    jenis = "MA"
                get_jenis[i].click()
                time.sleep(5)

                get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[1]/div/div[2]/input")

                get_data(browser, tahun, jenjang, jenis)
        elif jenjang == "SMK":
            jenis = "SMK"
            get_data(browser, tahun, jenjang, jenis)

        browser.quit()
    except Exception as ex:
        print(ex)
        browser.quit()

def get_data(browser, tahun, jenjang, jenis):
    get_infografis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div")
    for infografis in get_infografis:
        soup_infografis = BeautifulSoup(infografis.get_attribute("innerHTML"), "lxml")
        link_infografis = soup_infografis.find_all("a")
        
        for link in link_infografis:
            data = []
            provinsi = link.text.lstrip().rstrip()
            id_provinsi = query.get_id_provinsi(provinsi)

            data.append(id_provinsi)
            data.append(tahun)
            data.append(jenjang)
            data.append(jenis)
            data.append(link.get("href"))

            print(data)
            query.infografis(data)

links = [
        "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!infografis!99&99&999!T&01&1&T&1&!1!&",
        "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!infografis!99&99&999!T&01&1&T&1&!1!&",
        "https://hasilun.puspendik.kemdikbud.go.id/#2019!smk!infografis!99&99&999!T&01&1&T&1&!1!&"
        ]

with ProcessPoolExecutor(max_workers=1) as executor:
    futures = [ executor.submit(get_infografis_wilayah, url) for url in links ]
    results = []
    for result in as_completed(futures):
        results.append(result)