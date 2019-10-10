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
# initdb.create_prodi_matuji_db()

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
tahuns = ["2019", "2018"]
data = []

for jenjang in jenjangs:
    try:
        browser.get("https://hasilun.puspendik.kemdikbud.go.id/#2019!" + jenjang + "!capaian_wilayah!99&99&999!T&T&T&T&1&!1!&")
        time.sleep(5)

        get_jenjang = browser.find_element_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr/td/select/option[@selected='']")
        jenjang = BeautifulSoup(get_jenjang.get_attribute("innerHTML"), "lxml").get_text()

        get_matuji = BeautifulSoup(browser.find_element_by_xpath('//*[@id="matauji"]').get_attribute("innerHTML"), "lxml")
        list_matuji = get_matuji.find_all("option")

        if jenjang == "SMP/MTs" or jenjang == "SMK" or jenjang == "Paket B":
            # data = []
            prodi = jenjang

            id_prodi = query.get_id_prodi(prodi)
            data.append(id_prodi)

            for i in range(1, len(list_matuji)):
                matuji = list_matuji[i].text.lstrip()
                id_matuji = query.get_id_matuji(matuji)
                data.append(id_matuji)
                for tahun in tahuns:
                    data.append(tahun)
                    print(data)

                    query.prodi_matuji(data)

                    data.pop()
                data.pop()
            data.clear()
        elif jenjang == "SMA/MA" or jenjang == "Paket C":
            get_prodi = BeautifulSoup(browser.find_element_by_xpath('//*[@id="jurusan"]').get_attribute("innerHTML"), "lxml")
            list_prodi = get_prodi.find_all("option")
            for nama in list_prodi:
                prodi = nama.get_text().lstrip()

                id_prodi = query.get_id_prodi(prodi)
                data.append(id_prodi)

                select_prodi = Select(browser.find_element_by_xpath('//*[@id="jurusan"]'))
                select_prodi.select_by_visible_text(prodi)
                time.sleep(4)
                for i in range(1, len(list_matuji)):
                    if jenjang == "Paket C":
                        i = 7
                    get_matuji = BeautifulSoup(browser.find_element_by_xpath('//*[@id="matauji"]').get_attribute("innerHTML"), "lxml")
                    list_matuji = get_matuji.find_all("option")
                    matuji = list_matuji[i].text.lstrip()
                    id_matuji = query.get_id_matuji(matuji)
                    data.append(id_matuji)
                    for tahun in tahuns:
                        data.append(tahun)
                        print(data)

                        query.prodi_matuji(data)

                        data.pop()
                    data.pop()
                    if jenjang == "Paket C":
                        break
                data.clear()
    except Exception as ex:
        print(ex)

browser.quit()
