import time
from bs4 import BeautifulSoup
# import multiprocessing
import initheadless
import initdb
import query
from selenium.webdriver.support.ui import Select
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

db = initdb.get_db()
cursor = initdb.get_cursor(db)
# initdb.create_sekolah_db()

# manager = multiprocessing.Manager()

def log(text):
    print (text, file=open("log.txt", "a"))
    print (get_date(), file=open("log.txt", "a"))

def get_date():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt

# delete log
f = open("log.txt", "w").close()

#get moda ujian
browser = initheadless.headless_browser()
browser.get("https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&01&999!T&T&T&T&1&!3!&")
time.sleep(4)

try:
    get_moda_ujian = BeautifulSoup(browser.find_element_by_xpath('//*[@id="moda"]').get_attribute("innerHTML"), "lxml")
    list_moda = get_moda_ujian.find_all("option")
    for i in range(0, len(list_moda)):
        moda = []
        if i != 0:
            if list_moda[i].get_text() == "UNBK":
                nama = "Ujian Nasional Berbasis Komputer"
            else:
                nama = "Ujian Nasional Berbasis Kertas dan Pensil"
            moda.append(list_moda[i].get_text())
            moda.append(nama)
            print(moda)

            query.moda_ujian(moda)
    browser.quit()
except Exception as ex:
    print(ex)
    browser.quit()
    
# get smp
browser = initheadless.headless_browser()
browser.get("https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&01&999!T&T&1&T&1&unbk!3!&")
time.sleep(4)

loop_jenis = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td").get_attribute("innerHTML"), "lxml").find_all("input")
get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td/input")
for i in range(0, len(loop_jenis)-1):
    if i == 0:
        jenis = "SMP"
    elif i == 1:
        jenis = "MTs"
    else:
        jenis = "SMPT"

    get_jenis[i].click()
    time.sleep(2)
    # get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td[1]/input")

    for j in range(0, 2):
        moda = Select(browser.find_element_by_xpath('//*[@id="moda"]'))
        if j == 1:
            moda.select_by_visible_text("UNBK")
            time.sleep(2)
            id_moda = 1
        else:
            moda.select_by_visible_text("UNKP")
            time.sleep(2)
            id_moda = 2

        # keep element
        get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td[1]/input")

        get_tahun = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr/td[3]/select//option[@selected='']").get_attribute("innerHTML"), "lxml")
        tahun = get_tahun.get_text()

        try:
            get_id_kabupaten = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div[3]/div/div[2]/div/div[3]/table/thead/tr[3]/th[2]").get_attribute("innerHTML"), "lxml")
            id_kabupaten = get_id_kabupaten.get_text()

            get_jenjang = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr/td/select/option[@selected='']").get_attribute("innerHTML"), "lxml")
            jenjang = get_jenjang.get_text()

            get_sekolah = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div[3]/table/tbody/tr")
            for data_sekolah in get_sekolah:
                sekolah = []
                relasi_sekolahmoda = []
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

                # query di sini

                # get relasi sekolah moda
                relasi_sekolahmoda.append(sekolah[0])
                relasi_sekolahmoda.append(id_moda)
                relasi_sekolahmoda.append(tahun)
                print(relasi_sekolahmoda)

                # query di sini

        except Exception as ex:
            print(ex)
    
browser.quit()