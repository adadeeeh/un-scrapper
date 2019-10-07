import time
from bs4 import BeautifulSoup
# import multiprocessing
import initheadless
import initdb
import query
from selenium.webdriver.support.ui import Select
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

browser = initheadless.headless_browser()

db = initdb.get_db()
cursor = initdb.get_cursor(db)
initdb.create_sekolah_db()

# manager = multiprocessing.Manager()

def log(text, time):
    print (text, file=open("log.txt", "a"))
    print (time, file=open("log.txt", "a"))

def get_date():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt

# delete log
f = open("log.txt", "w").close()

#get moda ujian
browser.get("https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&01&999!T&T&T&T&1&!3!&")
time.sleep(4)

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

select = Select(browser.find_element_by_xpath('//*[@id="moda"]'))
select.all_selected_options
time.sleep(4)

# print(select_option.text)

browser.quit()