import time
from bs4 import BeautifulSoup
import initheadless
import initdb
import query
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

browser = initheadless.headless_browser()

db = initdb.get_db()
cursor = initdb.get_cursor(db)
# initdb.create_prov_kab_db()

def log(text):
    print (text, file=open("log.txt", "a"))
    print (get_date(), file=open("log.txt", "a"))

def get_date():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt

# delete log
f = open("log.txt", "w").close()

#provinsi
browser.get("https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!99&99&999!T&T&T&T&1&!1!&")
time.sleep(4)

get_jumlah_provinsi = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div[3]/table/tbody/tr")

for data_provinsi in get_jumlah_provinsi:
    try:
        provinsi = []
        soup_provinsi = BeautifulSoup(data_provinsi.get_attribute("innerHTML"), "lxml")
        list_provinsi = soup_provinsi.find_all(["td"])
        for i in range(1, 3):
            if i == 1:
                id_provinsi = list_provinsi[i].get_text() + "99"
                provinsi.append(id_provinsi)
            else:
                provinsi.append(list_provinsi[i].get_text())
        print(provinsi)

        # query.provinsi(provinsi)
        
    except Exception as ex:
        print(ex)

browser.quit()

#generate link kabupaten
url1 = "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!"
url2 = "&99&999!T&T&T&T&1&!2!&"
link_kabupaten = []
for i in range(1, 35):
    if i < 10:
        number = "0" + str(i)
    else:
        number = str(i)
    url = url1 + number + url2
    link_kabupaten.append(url)

def get_kabupaten(url):
    browser = initheadless.headless_browser()
    browser.get(url)
    time.sleep(4)

    get_jumlah_kabupaten = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div[3]/table/tbody/tr")
    get_id_provinsi = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div[3]/div/div[2]/div/div[3]/table/thead/tr[3]/th[2]").get_attribute("innerHTML"), "lxml")
    id_provinsi = get_id_provinsi.get_text()
    for data_kabupaten in get_jumlah_kabupaten:
        try:
            kabupaten = []
            soup_kabupaten = BeautifulSoup(data_kabupaten.get_attribute("innerHTML"), "lxml")
            list_kabupaten = soup_kabupaten.find_all(["td"])
            for i in range(1, 3):
                if i == 1:
                    id_kabupaten = list_kabupaten[i].get_text() + "999"
                    kabupaten.append(id_kabupaten)
                else:
                    kabupaten.append(id_provinsi)
                    kabupaten.append(list_kabupaten[i].get_text())
            print(kabupaten)
            
            # query.kabupaten(kabupaten)

        except Exception as ex:
            print(ex)

    browser.quit()

with ProcessPoolExecutor(max_workers=5) as executor:
    futures = [ executor.submit(get_kabupaten, url) for url in link_kabupaten ]
    results = []
    for result in as_completed(futures):
        results.append(result)