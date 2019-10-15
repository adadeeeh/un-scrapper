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
# initdb.create_materiujian_indikatormateri()

def log(text):
    print (text, file=open("log.txt", "a"))
    print (get_date(), file=open("log.txt", "a"))

def get_date():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt

# delete log
f = open("log.txt", "w").close()

jenjangs = ["smp", "sma", "smk", "paketc", "paketb"]
tahuns = ["2019", "2018"]
browser = initheadless.headless_browser()

for tahun in tahuns:
    for jenjang in jenjangs:
        try:
            if (jenjang == "paketc" and tahun == "2019") or (jenjang == "paketc" and tahun == "2018") or (jenjang == "paketb" and tahun == "2019") or (jenjang == "paketb" and tahun == "2018"):
                continue
            browser.get("https://hasilun.puspendik.kemdikbud.go.id/#" + tahun + "!" + jenjang + "!daya_serap!99&99&999!T&T&T&T&1&!1!&")
            time.sleep(5)

            get_jenjang = browser.find_element_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr/td/select/option[@selected='']")
            jenjang = BeautifulSoup(get_jenjang.get_attribute("innerHTML"), "lxml").get_text()

            get_matuji = BeautifulSoup(browser.find_element_by_xpath('//*[@id="matauji"]').get_attribute("innerHTML"), "lxml")
            list_matuji = get_matuji.find_all("option")
            select = Select(browser.find_element_by_xpath('//*[@id="matauji"]'))
            for matuji in list_matuji:
                select.select_by_visible_text(matuji.text.lstrip())
                time.sleep(5)
                select = Select(browser.find_element_by_xpath('//*[@id="matauji"]'))

                matuji = matuji.text.lstrip()
                id_matuji = query.get_id_matuji(matuji)
                print(matuji, id_matuji)

                get_jumlah_materi = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div[2]/table/tbody/tr/td[2]")
                for materi in get_jumlah_materi:
                    soup_materi = BeautifulSoup(materi.get_attribute("innerHTML"), "lxml")
                    print(soup_materi.get_text())
                
        except Exception as ex:
            print(ex)
browser.quit()