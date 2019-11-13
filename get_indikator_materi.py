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
# initdb.create_indikator_db()

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

def get_indikator():
    get_matuji = BeautifulSoup(browser.find_element_by_xpath('//*[@id="matauji"]').get_attribute("innerHTML"), "lxml")
    list_matuji = get_matuji.find_all("option")
    select = Select(browser.find_element_by_xpath('//*[@id="matauji"]'))
    for matuji in list_matuji:
        if matuji.text.lstrip() == "DOKTRIN GEREJA KATOLIK & MORAL KRISTIANI":
            continue
        select.select_by_visible_text(matuji.text.lstrip())
        time.sleep(15)
        select = Select(browser.find_element_by_xpath('//*[@id="matauji"]'))

        # indikator materi
        try:
            data = []
            number = ["1", "2", "3", "4", "5", "6", "7", "8"]
            # id_materi = query.get_id_materi(materi)
            # print(id_materi)
            get_indikator = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div[6]/table/tbody/tr")
            for i in get_indikator:
                soup_indikator = BeautifulSoup(i.get_attribute("innerHTML"), "lxml")
                list_indikator = soup_indikator.find_all("td", {"class": "text-left"})
                for text in list_indikator:
                    # print(indikator.text)
                    if text.text[0] in number:
                        materi = text.text.split(".")
                        materi = materi[1].lstrip()
                        id_materi = query.get_id_materi(materi)
                        print(id_materi, materi)
                    else:
                        indikator = text.text
                        data.append(id_materi)
                        data.append(indikator)
                        
                        item = 0
                        id_materi2 = query.get_id_materi_by_indikator(indikator)
                        for item in id_materi2:
                            if item[0] == id_materi:
                                item = id_materi
                                break
                        
                        if item == id_materi:
                            data.clear()
                            break

                        print(data)
                        # query.indikator_materi(data)
                        data.clear()
                        
        except Exception as ex:
            print(ex)

for tahun in tahuns:
    for jenjang in jenjangs:
        # if (jenjang == "paketc" and tahun == "2019") or (jenjang == "paketc" and tahun == "2018") or (jenjang == "paketb" and tahun == "2019") or (jenjang == "paketb" and tahun == "2018"):
        #         continue
        browser.get("https://hasilun.puspendik.kemdikbud.go.id/#" + tahun + "!" + jenjang + "!daya_serap!99&99&999!T&T&T&T&1&!1!&")
        time.sleep(5)
        # materi ujian
        try:
            get_jenjang = browser.find_element_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr/td/select/option[@selected='']")
            jenjang = BeautifulSoup(get_jenjang.get_attribute("innerHTML"), "lxml").get_text()

            if jenjang == "SMA/MA" or jenjang == "Paket C":
                get_prodi = BeautifulSoup(browser.find_element_by_xpath('//*[@id="jurusan"]').get_attribute("innerHTML"), "lxml")
                list_prodi = get_prodi.find_all("option")
                select_prodi = Select(browser.find_element_by_xpath('//*[@id="jurusan"]'))
                for prodi in list_prodi:
                    select_prodi = Select(browser.find_element_by_xpath('//*[@id="jurusan"]'))
                    # print(prodi.text.lstrip())
                    select_prodi.select_by_visible_text(prodi.text.lstrip())
                    time.sleep(5)
                    get_indikator()
            else:
                get_indikator()
        except Exception as ex:
            print(ex)

browser.quit()