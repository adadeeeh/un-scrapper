import time
from bs4 import BeautifulSoup
import initheadless
import initdb
import query
from selenium.webdriver.support.ui import Select
from datetime import datetime

db = initdb.get_db()
cursor = initdb.get_cursor(db)
initdb.create_independent_db()

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

#get prodi
browser = initheadless.headless_browser()
browser.get("https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!99&99&999!T&T&T&T&1&!1!&")
time.sleep(4)

get_loop_jenjang = browser.find_element_by_xpath('//*[@id="page"]')
soup_loop_jenjang = BeautifulSoup(get_loop_jenjang.get_attribute("innerHTML"), "lxml")
loop_jenjang = soup_loop_jenjang.find_all("option")

for loop in loop_jenjang:
    try:
        select = Select(browser.find_element_by_xpath('//*[@id="page"]'))
        select.select_by_visible_text(loop.get_text())
        time.sleep(2)
        get_jenjang = browser.find_element_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr/td/select/option[@selected='']")
        jenjang = BeautifulSoup(get_jenjang.get_attribute("innerHTML"), "lxml").get_text()
        if jenjang == "SMP/MTs" or jenjang == "SMK" or jenjang == "Paket B":
            prodi = jenjang
            print(prodi)

            query.prodi(prodi)

        elif jenjang == "Paket C":
            continue
        else:
            get_prodi = browser.find_elements_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td/select/option")
            for nama in get_prodi:
                prodi = BeautifulSoup(nama.get_attribute("innerHTML"), "lxml").get_text()
                print(prodi)

                query.prodi(prodi)

    except Exception as ex:
        print(ex)
browser.quit()

#get mata ujian
browser = initheadless.headless_browser()
jenjang = ["smp", "sma", "smk", "paketb"]
for item in jenjang:
    browser.get("https://hasilun.puspendik.kemdikbud.go.id/#2019!" + item + "!daya_serap!99&99&999!T&T&T&T&1&!1!&")
    time.sleep(10)

    try:
        if item == "sma":
            get_prodi = BeautifulSoup(browser.find_element_by_xpath('//*[@id="jurusan"]').get_attribute("innerHTML"), "lxml")
            list_prodi = get_prodi.find_all("option")
            for i in range(0, len(list_prodi)):
                select = Select(browser.find_element_by_xpath('//*[@id="jurusan"]'))
                select.select_by_visible_text(list_prodi[i].text.lstrip())
                time.sleep(10)
                
                get_matuji = BeautifulSoup(browser.find_element_by_xpath('//*[@id="matauji"]').get_attribute("innerHTML"), "lxml")
                list_matuji = get_matuji.find_all("option")
                for i in range(3, len(list_matuji)):
                    print(list_matuji[i].text.lstrip())
                    matuji = list_matuji[i].text.lstrip()

                    query.matuji(matuji)
        elif item == "smp":
            get_matuji = BeautifulSoup(browser.find_element_by_xpath('//*[@id="matauji"]').get_attribute("innerHTML"), "lxml")
            list_matuji = get_matuji.find_all("option")
            for i in range(0, len(list_matuji)-1):
                print(list_matuji[i].text.lstrip())
                matuji = list_matuji[i].text.lstrip()

                query.matuji(matuji)
        else:
            get_matuji = BeautifulSoup(browser.find_element_by_xpath('//*[@id="matauji"]').get_attribute("innerHTML"), "lxml")
            list_matuji = get_matuji.find_all("option")
            for i in range(3, len(list_matuji)):
                print(list_matuji[i].text.lstrip())
                matuji = list_matuji[i].text.lstrip()

                query.matuji(matuji)
    except Exception as ex:
        print(ex)

    

browser.quit()
