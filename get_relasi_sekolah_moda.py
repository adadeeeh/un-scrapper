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
# initdb.create_relasi_sekolah_moda_db()

def log(text):
    print (text, file=open("log.txt", "a"))
    print (get_date(), file=open("log.txt", "a"))

def get_date():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt

# delete log
f = open("log.txt", "w").close()

def get_relasi(url):
    try:
        browser = initheadless.headless_browser()
        browser.get(url)
        time.sleep(5)
        
        select_jenjang = Select(browser.find_element_by_id("page"))
        jenjang = select_jenjang.first_selected_option.text
        if jenjang == "SMP/MTs" or jenjang == "SMK" or jenjang == "Paket B":
            if jenjang == "Paket B":
                moda = "UNKP"
            else:
                select_moda = Select(browser.find_element_by_id("moda"))
                moda = select_moda.first_selected_option.text
            get_data(browser, moda)
        if jenjang == "SMA/MA" or jenjang == "Paket C":
            if jenjang == "Paket C":
                moda = "UNKP"
            else:
                select_moda = Select(browser.find_element_by_id("moda"))
                moda = select_moda.first_selected_option.text
            loop_prodi = BeautifulSoup(browser.find_element_by_id("jurusan").get_attribute("innerHTML"), "lxml").find_all("option")
            select_prodi = Select(browser.find_element_by_id("jurusan"))
            for prodi in loop_prodi:
                select_prodi.select_by_visible_text(prodi.text.lstrip())
                time.sleep(7)
                get_data(browser, moda)
                select_prodi = Select(browser.find_element_by_id("jurusan"))

        browser.quit()
    except Exception as ex:
        print(ex)
        browser.quit()

def get_data(browser, moda):
    select_tahun = Select(browser.find_element_by_id("tahun"))
    tahun = select_tahun.first_selected_option.text
    id_moda = query.get_id_moda(moda)
    get_sekolah = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div[3]/table/tbody/tr")
    for data_sekolah in get_sekolah:
        data_relasi = []
        soup_sekolah = BeautifulSoup(data_sekolah.get_attribute("innerHTML"), "lxml")
        list_sekolah = soup_sekolah.find_all("td")
        nama_sekolah = list_sekolah[2].text
        id_sekolah = query.get_id_sekolah(nama_sekolah)
        if id_sekolah == None:
            continue
        data_relasi.append(id_sekolah)
        data_relasi.append(id_moda)
        data_relasi.append(tahun)
        
        #check data if exists
        cek_id = query.get_id_relasi_sekolah_moda(data_relasi)
        if cek_id == id_sekolah:
           continue

        print(data_relasi)
        query.relasi_sekolah_moda(data_relasi)

links = [
            "https://hasilun.puspendik.kemdikbud.go.id/#2018!sma!capaian!01&99&999!T&T&T&T&1&unbk!3!&",
            "https://hasilun.puspendik.kemdikbud.go.id/#2018!sma!capaian!01&99&999!T&T&T&T&1&unkp!3!&",
            "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!capaian!01&99&999!T&T&T&T&1&unbk!3!&",
            "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!capaian!01&99&999!T&T&T&T&1&unkp!3!&"
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&99&999!T&T&T&T&1&unbk!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&99&999!T&T&T&T&1&unkp!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!capaian!01&99&999!b&T&T&T&1&unbk!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!capaian!01&99&999!b&T&T&T&1&unkp!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smk!capaian!01&99&999!T&T&1&T&1&unbk!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smk!capaian!01&99&999!T&T&1&T&1&unkp!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!paketb!capaian!01&99&999!T&T&T&T&1&!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!paketc!capaian!01&99&999!T&T&T&T&1&!3!&"
        ]

jenjangs = ["smp"]
modas = ["unbk", "unkp"]
tahuns = ["2019", "2018"]
for jenjang in jenjangs:
    for moda in modas:
        for tahun in tahuns:
            for i in range(1, 35):
                if i < 10:
                    i = "0"+str(i)
                    if jenjang == "paketb" or jenjang == "paketc":
                        url = f'https://hasilun.puspendik.kemdikbud.go.id/#2019!{jenjang}!capaian!{i}&99&999!T&T&T&T&1&!3!&'
                        # links.append(url)
                    else:
                        url = f'https://hasilun.puspendik.kemdikbud.go.id/#2019!{jenjang}!capaian!{i}&99&999!T&T&1&T&1&{moda}!3!&'
                        # links.append(url)
                elif i >= 10:
                    if jenjang == "paketb" or jenjang == "paketc":
                        url = f'https://hasilun.puspendik.kemdikbud.go.id/#2019!{jenjang}!capaian!{i}&99&999!T&T&T&T&1&!3!&'
                        # links.append(url)
                    else:
                        url = f'https://hasilun.puspendik.kemdikbud.go.id/#2019!{jenjang}!capaian!{i}&99&999!T&T&1&T&1&{moda}!3!&'
                        # links.append(url)

with ProcessPoolExecutor(max_workers=1) as executor:
    futures = [ executor.submit(get_relasi, url) for url in links ]
    results = []
    for result in as_completed(futures):
        results.append(result)