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
# initdb.create_sekolah_memiliki_prodi_db()

def log(text):
    print (text, file=open("log.txt", "a"))
    print (get_date(), file=open("log.txt", "a"))

def get_date():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt

# delete log
f = open("log.txt", "w").close()

def get_sekolah_prodi(url):
    try:
        browser = initheadless.headless_browser()
        browser.get(url)
        time.sleep(5)

        tahuns = ["2019", "2018"]
        for tahun in tahuns:
            if tahun in url:
                tahun = tahun
                break

        select_jenjang = Select(browser.find_element_by_id("page"))
        jenjang = select_jenjang.first_selected_option.text
        if jenjang == "SMP/MTs" or jenjang == "SMK" or jenjang == "Paket B":
            id_prodi = query.get_id_prodi(jenjang)
            get_data(browser, id_prodi, tahun)
        elif jenjang == "SMA/MA" or jenjang == "Paket C":
            get_prodi = BeautifulSoup(browser.find_element_by_id("jurusan").get_attribute("innerHTML"), "lxml")
            list_prodi = get_prodi.find_all("option")
            select_prodi = Select(browser.find_element_by_id("jurusan"))
            prodi = select_prodi.first_selected_option.text
            for prodi in list_prodi:
                prodi = prodi.text.lstrip()
                select_prodi.select_by_visible_text(prodi)
                id_prodi = query.get_id_prodi(prodi)
                time.sleep(5)

                get_data(browser, id_prodi, tahun)

                select_prodi = Select(browser.find_element_by_id("jurusan"))
        browser.quit()
    except Exception as ex:
        print(ex)
        browser.quit()

def get_data(browser, id_prodi, tahun):
    get_sekolah = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div[3]/table/tbody/tr")
    for data_sekolah in get_sekolah:
        data = []
        soup_sekolah = BeautifulSoup(data_sekolah.get_attribute("innerHTML"), "lxml").find_all("td")
        nama_sekolah = soup_sekolah[2].text
        id_sekolah = query.get_id_sekolah(nama_sekolah)
        jumlah_peserta = soup_sekolah[5].text

        if jumlah_peserta == "0":
            continue
        if id_sekolah == None:
            continue

        data.append(id_sekolah)
        data.append(id_prodi)
        data.append(jumlah_peserta)
        data.append(tahun)

        #check data if exists
        cek_id = query.get_id_relasi_sekolah_prodi(data)
        if cek_id == id_sekolah:
           continue

        print(data)
        query.relasi_sekolah_memiliki_prodi(data)


links = [
        "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&99&999!T&T&T&T&1&!3!&",
        # "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!capaian!01&99&999!T&T&T&T&1&!3!&",
        # "https://hasilun.puspendik.kemdikbud.go.id/#2018!sma!capaian!01&99&999!T&T&T&T&1&!3!&",
        # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smk!capaian!01&99&999!T&T&T&T&1&!3!&",
        # "https://hasilun.puspendik.kemdikbud.go.id/#2019!paketc!capaian!01&99&999!T&T&T&T&1&!3!&",
        # "https://hasilun.puspendik.kemdikbud.go.id/#2019!paketb!capaian!01&99&999!T&T&T&T&1&!3!&"
        ]

jenjangs = ["smp", "sma", "smk", "paketb", "paketc"]
tahuns = ["2019", "2018"]
for jenjang in jenjangs:
    for tahun in tahuns:
        for i in range(1, 35):
            if i < 10:
                i = "0"+str(i)
                if jenjang == "paketb" or jenjang == "paketc":
                    url = f'https://hasilun.puspendik.kemdikbud.go.id/#{tahun}!{jenjang}!capaian!{i}&99&999!T&T&T&T&1&!3!&'
                    links.append(url)
                else:
                    url = f'https://hasilun.puspendik.kemdikbud.go.id/#{tahun}!{jenjang}!capaian!{i}&99&999!T&T&T&T&1&!3!&'
                    links.append(url)
            elif i >= 10:
                if jenjang == "paketb" or jenjang == "paketc":
                    url = f'https://hasilun.puspendik.kemdikbud.go.id/#{tahun}!{jenjang}!capaian!{i}&99&999!T&T&T&T&1&!3!&'
                    links.append(url)
                else:
                    url = f'https://hasilun.puspendik.kemdikbud.go.id/#{tahun}!{jenjang}!capaian!{i}&99&999!T&T&T&T&1&!3!&'
                    links.append(url)
            # if i < 10:
            #     i = "0"+str(i)
            # url = f'https://hasilun.puspendik.kemdikbud.go.id/#{tahun}!{jenjang}!capaian!{i}&99&999!T&T&T&T&1&!3!&'
            # links.append(url)

with ProcessPoolExecutor(max_workers=1) as executor:
    futures = [ executor.submit(get_sekolah_prodi, url) for url in links ]
    results = []
    for result in as_completed(futures):
        results.append(result)