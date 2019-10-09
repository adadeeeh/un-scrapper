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
# initdb.create_independent_db()

def log(text):
    print (text, file=open("log.txt", "a"))
    print (get_date(), file=open("log.txt", "a"))

def get_date():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt

# delete log
f = open("log.txt", "w").close()

browser = initheadless.headless_browser()
jenjangs = ["smp", "sma", "smk", "paketb", "paketc"]

for jenjang in jenjangs:
    browser.get("https://hasilun.puspendik.kemdikbud.go.id/#2019!" + jenjang + "!capaian_wilayah!99&99&999!T&T&T&T&1&!1!&")
    time.sleep(4)

    get_jenjang = browser.find_element_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr/td/select/option[@selected='']")
    jenjang = BeautifulSoup(get_jenjang.get_attribute("innerHTML"), "lxml").get_text()
    if jenjang == "SMP/MTs" or jenjang == "SMK" or jenjang == "Paket B":
        prodi = jenjang

        id_prodi = query.get_id_prodi(prodi)
        print(id_prodi[0])
    elif jenjang == "Paket C":
        continue
    else:
        get_prodi = BeautifulSoup(browser.find_element_by_xpath('//*[@id="jurusan"]').get_attribute("innerHTML"), "lxml")
        list_prodi = get_prodi.find_all("option")
        for nama in list_prodi:
            prodi = nama.get_text().lstrip()

            id_prodi = query.get_id_prodi(prodi)
            print(id_prodi[0])

browser.quit()
