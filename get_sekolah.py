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
initdb.create_sekolah_db()

def log(text):
    print (text, file=open("log.txt", "a"))
    print (get_date(), file=open("log.txt", "a"))

def get_date():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt

# delete log
f = open("log.txt", "w").close()

def get_sekolah(url):    
    try:
        browser = initheadless.headless_browser()
        browser.get(url)
        time.sleep(5)

        get_provinsi = BeautifulSoup(browser.find_element_by_id("provinsi").get_attribute("innerHTML"), "lxml")
        list_provinsi = get_provinsi.find_all("option")
        select_provinsi = Select(browser.find_element_by_id("provinsi"))
        for provinsi in list_provinsi:
            provinsi = provinsi.text.lstrip()
            select_provinsi.select_by_visible_text(provinsi)
            time.sleep(5)

            get_kota = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div/div/div/div/table/tbody/tr[2]/td[3]/select").get_attribute("innerHTML"), "lxml")
            list_kota = get_kota.find_all("option")
            select_kota = Select(browser.find_element_by_id("rayon"))
            for i in range(0, len(list_kota)):
                if i > 0:
                    kota = list_kota[i].text.lstrip()
                    select_kota.select_by_visible_text(kota)
                    time.sleep(5)

                    get_jenjang = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr/td/select/option[@selected='']").get_attribute("innerHTML"), "lxml")
                    jenjang = get_jenjang.get_text()
                    
                    if jenjang == "SMP/MTs" or jenjang == "SMK":
                        loop_jenis = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td").get_attribute("innerHTML"), "lxml").find_all("input")
                        get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td/input")
                        if jenjang == "SMP/MTs":
                            loop = len(loop_jenis)-1
                        elif jenjang == "SMK":
                            loop = len(loop_jenis)
                        for i in range(0, loop):
                            if i == 0 and jenjang == "SMP/MTs":
                                jenis = "SMP"
                            elif i == 1 and jenjang == "SMP/MTs":
                                jenis = "MTs"
                            elif i == 2 and jenjang == "SMP/MTs":
                                jenis = "SMPT"
                            elif i == 0 and jenjang == "SMK":
                                jenis = "SMK"
                            get_jenis[i].click()
                            time.sleep(5)
                            
                            get_id_kabupaten = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div[3]/div/div[2]/div/div[3]/table/thead/tr[3]/th[2]").get_attribute("innerHTML"), "lxml")
                            id_kabupaten = get_id_kabupaten.get_text()

                            get_sekolah = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div[3]/table/tbody/tr")
                            for data_sekolah in get_sekolah:
                                sekolah = []
                                soup_sekolah = BeautifulSoup(data_sekolah.get_attribute("innerHTML"), "lxml")
                                list_sekolah = soup_sekolah.find_all("td")
                                for k in range(1, 5):
                                    sekolah.append(list_sekolah[k].get_text())
                                sekolah.insert(1, id_kabupaten)
                                sekolah.insert(3, jenjang)
                                npsn = sekolah.pop(4)
                                sekolah.append(npsn)
                                sekolah.insert(4, jenis)
                                print(sekolah)

                                query.sekolah(sekolah)
                            
                            get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td[1]/input")
                            select_kota = Select(browser.find_element_by_id("rayon"))
                            select_provinsi = Select(browser.find_element_by_id("provinsi"))
        browser.quit()
    except Exception as ex:
        print(ex)
        browser.quit()

def get_data(browser, jenis, jenjang):
    try:
        get_id_kabupaten = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div[3]/div/div[2]/div/div[3]/table/thead/tr[3]/th[2]").get_attribute("innerHTML"), "lxml")
        id_kabupaten = get_id_kabupaten.get_text()

        get_sekolah = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div[3]/table/tbody/tr")
        for data_sekolah in get_sekolah:
            sekolah = []
            soup_sekolah = BeautifulSoup(data_sekolah.get_attribute("innerHTML"), "lxml")
            list_sekolah = soup_sekolah.find_all("td")
            for k in range(1, 5):
                sekolah.append(list_sekolah[k].get_text())
            sekolah.insert(1, id_kabupaten)
            sekolah.insert(3, jenjang)
            npsn = sekolah.pop(4)
            sekolah.append(npsn)
            sekolah.insert(4, jenis)
            print(sekolah)

            query.sekolah(sekolah)
    except Exception as ex:
        print(ex)

links = [
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&01&999!T&T&1&T&1&unbk!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&01&999!T&T&1&T&1&unkp!3!&",
            "https://hasilun.puspendik.kemdikbud.go.id/#2019!smk!capaian!01&01&999!T&T&1&T&1&unbk!3!&"
        ]

with ProcessPoolExecutor(max_workers=1) as executor:
    futures = [ executor.submit(get_sekolah, url) for url in links ]
    results = []
    for result in as_completed(futures):
        results.append(result)


