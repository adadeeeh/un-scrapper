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
# initdb.create_sekolah_db()

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

        # get_provinsi = BeautifulSoup(browser.find_element_by_id("provinsi").get_attribute("innerHTML"), "lxml")
        # list_provinsi = get_provinsi.find_all("option")
        # select_provinsi = Select(browser.find_element_by_id("provinsi"))
        # for provinsi in list_provinsi:
        #     provinsi = provinsi.text.lstrip()
        #     select_provinsi.select_by_visible_text(provinsi)
        #     time.sleep(5)

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
                    if jenjang == "SMP/MTs" or jenjang == "Paket B":
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
                        
                        get_data(browser, jenjang, jenis)
                        
                        get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td[1]/input")
                        select_kota = Select(browser.find_element_by_id("rayon"))
                        # select_provinsi = Select(browser.find_element_by_id("provinsi"))
                if jenjang == "Paket B":
                    jenis = ""
                    get_data(browser, jenjang, jenis)
                    
                    get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td[1]/input")
                    select_kota = Select(browser.find_element_by_id("rayon"))
                    # select_provinsi = Select(browser.find_element_by_id("provinsi"))
                if jenjang == "SMA/MA":
                    loop_jenis = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td[2]").get_attribute("innerHTML"), "lxml").find_all("input")
                    get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td[2]/input")
                    if jenjang == "SMA/MA":
                        loop = len(loop_jenis)-1
                    for i in range(0, loop):
                        if i == 0:
                            jenis = "SMA"
                        elif i == 1:
                            jenis = "MA"
                        get_jenis[i].click()
                        time.sleep(5)
                        
                        loop_prodi = BeautifulSoup(browser.find_element_by_id("jurusan").get_attribute("innerHTML"), "lxml").find_all("option")
                        select_prodi = Select(browser.find_element_by_id("jurusan"))
                        for prodi in loop_prodi:
                            select_prodi.select_by_visible_text(prodi.text.lstrip())
                            time.sleep(7)

                            get_data(browser, jenjang, jenis)
                            
                            get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td[2]/input")
                            select_kota = Select(browser.find_element_by_id("rayon"))
                            # select_provinsi = Select(browser.find_element_by_id("provinsi"))
                            select_prodi = Select(browser.find_element_by_id("jurusan"))
                if jenjang == "Paket C":
                    loop_prodi = BeautifulSoup(browser.find_element_by_id("jurusan").get_attribute("innerHTML"), "lxml").find_all("option")
                    select_prodi = Select(browser.find_element_by_id("jurusan"))
                    jenis = ""
                    for prodi in loop_prodi:
                        select_prodi.select_by_visible_text(prodi.text.lstrip())
                        time.sleep(7)

                        get_data(browser, jenjang, jenis)
                        
                        get_jenis = browser.find_elements_by_xpath("//div[3]/div[3]/div/div/div/table/tbody/tr[3]/td[2]/input")
                        select_kota = Select(browser.find_element_by_id("rayon"))
                        # select_provinsi = Select(browser.find_element_by_id("provinsi"))
                        select_prodi = Select(browser.find_element_by_id("jurusan"))
        browser.quit()
    except Exception as ex:
        print(ex)
        browser.quit()

def get_data(browser, jenjang, jenis):
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
        if jenjang == "Paket B" or jenjang == "Paket C":
            nama_sekolah = sekolah[2]
            split_nama = nama_sekolah.split(" ")
            if split_nama[0] == "PKBM":
                jenis = "PKBM"
            else:
                jenis = "PONPES"
            sekolah.pop(4)
            sekolah.insert(4, jenis)
        if jenjang == "Paket C":
            sekolah[0] = "C" + sekolah[0]
        if jenjang == "SMP/MTs":
            sekolah[0] = "SMP" + sekolah[0]
        if jenjang == "SMA/MA":
            sekolah[0] = "SMA" + sekolah[0]
        if jenjang == "SMK":
            sekolah[0] = "SMK" + sekolah[0]
        if jenjang == "Paket B":
            sekolah[0] = "B" + sekolah[0]
        id_sekolah = query.get_id_sekolah(sekolah[2])
        if id_sekolah:
            continue
        print(sekolah)
        try:
            query.sekolah(sekolah)
        except:
            pass

links = [
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&01&999!T&T&1&T&1&!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&01&999!T&T&1&T&1&unkp!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!capaian!01&99&999!b&T&T&T&1&!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!capaian!01&99&999!b&T&T&T&1&unkp!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smk!capaian!01&01&999!T&T&1&T&1&!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smk!capaian!01&01&999!T&T&1&T&1&unkp!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!paketb!capaian!01&01&999!T&T&T&T&1&!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!paketc!capaian!01&01&999!T&T&T&T&1&!3!&"
        ]

jenjangs = ["smp"]
#"smp", "sma", "smk", "paketb", "paketc"
for jenjang in jenjangs:
    for i in range(1, 2):
        if i < 10:
            i = "0"+str(i)
            if jenjang == "paketb" or jenjang == "paketc":
                url = f'https://hasilun.puspendik.kemdikbud.go.id/#2019!{jenjang}!capaian!{i}&01&999!T&T&T&T&1&!3!&'
                links.append(url)
            else:
                url = f'https://hasilun.puspendik.kemdikbud.go.id/#2019!{jenjang}!capaian!{i}&01&999!T&T&1&T&1&!3!&'
                links.append(url)
        elif i >= 10:
            if jenjang == "paketb" or jenjang == "paketc":
                url = f'https://hasilun.puspendik.kemdikbud.go.id/#2019!{jenjang}!capaian!{i}&01&999!T&T&T&T&1&!3!&'
                links.append(url)
            else:
                url = f'https://hasilun.puspendik.kemdikbud.go.id/#2019!{jenjang}!capaian!{i}&01&999!T&T&1&T&1&!3!&'
                links.append(url)

with ProcessPoolExecutor(max_workers=1) as executor:
    futures = [ executor.submit(get_sekolah, url) for url in links ]
    results = []
    for result in as_completed(futures):
        results.append(result)


