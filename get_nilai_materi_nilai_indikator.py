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
# initdb.create_nilai_materi_db()
# initdb.create_nilai_indikator_db()

def log(text):
    print (text, file=open("log.txt", "a"))
    print (get_date(), file=open("log.txt", "a"))

def get_date():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt

# delete log
f = open("log.txt", "w").close()

def get_nilai_materi(url):
    try:
        browser = initheadless.headless_browser()
        browser.get(url)
        time.sleep(5)

        get_kota = BeautifulSoup(browser.find_element_by_xpath("//div[3]/div[3]/div/div[1]/div/table/tbody/tr[2]/td[2]/select").get_attribute("innerHTML"), "lxml")
        list_kota = get_kota.find_all("option")
        list_kota.pop(0)
        select_kota = Select(browser.find_element_by_id("rayon"))
        for kota in list_kota:
            select_kota.select_by_visible_text(kota.text.lstrip())
            time.sleep(5)

            list_sekolah = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[1]/div/table/tbody/tr[2]/td[3]/select/option")
            list_sekolah.pop(0)
            select_sekolah = Select(browser.find_element_by_id("sekolah"))
            for i in range(0, len(list_sekolah)):
                sekolah = BeautifulSoup(list_sekolah[i].get_attribute("innerHTML"), "lxml").get_text()
                select_sekolah.select_by_visible_text(sekolah)
                time.sleep(5)

                # get tahun
                if "2019" in url:
                    tahun = "2019"
                elif "2018" in url:
                    tahun = "2018"

                # get id sekolah
                sekolah = sekolah.split(" ", 1)
                id_sekolah = query.get_id_sekolah(sekolah[1])
                
                # cek id sekolah
                if not id_sekolah:
                    list_sekolah = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[1]/div/table/tbody/tr[2]/td[3]/select/option")
                    list_sekolah.pop(0)
                    select_sekolah = Select(browser.find_element_by_id("sekolah"))
                    continue

                # get id prodi
                select_jenjang = Select(browser.find_element_by_id("page"))
                jenjang = select_jenjang.first_selected_option.text
                if jenjang == "SMP/MTs":
                    prodi = "SMP/MTs"
                    id_prodi = query.get_id_prodi(prodi)
                    get_data(browser, id_prodi, id_sekolah, tahun)
                elif jenjang == "SMA/MA" or jenjang == "Paket C":
                    select_prodi = Select(browser.find_element_by_id("jurusan"))
                    prodi = select_prodi.first_selected_option.text
                    id_prodi = query.get_id_prodi(prodi)
            
                    get_data(browser, id_prodi, id_sekolah, tahun)
                elif jenjang == "SMK":
                    prodi = "SMK"
                    id_prodi = query.get_id_prodi(prodi)
                    get_data(browser, id_prodi, id_sekolah, tahun)
                elif jenjang == "Paket B":
                    prodi = "Paket B"
                    id_prodi = query.get_id_prodi(prodi)
                    get_data(browser, id_prodi, id_sekolah, tahun)

                list_sekolah = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[1]/div/table/tbody/tr[2]/td[3]/select/option")
                list_sekolah.pop(0)
                select_sekolah = Select(browser.find_element_by_id("sekolah"))

            select_kota = Select(browser.find_element_by_id("rayon"))
        browser.quit()
    except Exception as ex:
        print(ex)
        print(url)
        browser.quit()

def get_data(browser, id_prodi, id_sekolah, tahun):
    list_matuji = BeautifulSoup(browser.find_element_by_id("matauji").get_attribute("innerHTML"), "lxml").find_all("option")
    select_matuji = Select(browser.find_element_by_id("matauji"))
    for matuji in list_matuji:
        matuji = matuji.text.lstrip()
        select_matuji.select_by_visible_text(matuji)
        time.sleep(5)
        select_matuji = Select(browser.find_element_by_id("matauji"))
        id_matuji = query.get_id_matuji(matuji)

        # get tabel nilai materi
        get_tabel_materi = browser.find_elements_by_xpath("/html/body/div[3]/div[3]/div/div[2]/div/div[2]/table/tbody/tr")
        for data_materi in get_tabel_materi:
            # print("Nilai Materi")
            data = []
            data_materi = BeautifulSoup(data_materi.get_attribute("innerHTML"), "lxml")
            data_materi = data_materi.find_all("td")
            materi = data_materi[1].text
            nilai = data_materi[2].text

            id_materi = query.get_id_materi(materi)
            
            data.append(id_materi)
            data.append(id_matuji)
            data.append(id_prodi)
            data.append(id_sekolah)
            data.append(nilai)
            data.append(tahun)

            #cek data if exist
            id_avgmateri = query.get_id_nilai_materi(data)
            if id_avgmateri:
                continue

            query.nilai_materi(data)
            print(data)        

        # get tabel nilai indikator
        get_indikator = browser.find_elements_by_xpath("//div[3]/div[3]/div/div[2]/div/div[6]/table/tbody/tr")
        for i in get_indikator:
            # print("Nilai Indikator")
            data = []
            data_indikator = BeautifulSoup(i.get_attribute("innerHTML"), "lxml").find_all("td")
            if len(data_indikator) < 2:
                materi = data_indikator[0].text.split(" ", 1)
                id_materi = query.get_id_materi(materi[1])
            else:
                indikator = data_indikator[1].text
                id_indikator = query.get_id_indikator(indikator)

                nilai = data_indikator[2].text

                data.append(id_indikator)
                data.append(id_matuji)
                data.append(id_materi)
                data.append(id_prodi)
                data.append(id_sekolah)
                data.append(nilai)
                data.append(tahun)

                #cek data if exist
                id_avgindikator = query.get_id_nilai_indikator(data)
                if id_avgindikator:
                    continue

                query.nilai_indikator(data)
                print(data)

links = [
        # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!daya_serap!01&99&999!T&01&1&T&1&!3!&"
        # "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!daya_serap!01&99&999!a&01&1&T&1&!3!&",
        # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smk!daya_serap!01&99&999!T&01&1&T&1&!3!&",
        # "https://hasilun.puspendik.kemdikbud.go.id/#2019!paketc!daya_serap!01&99&999!a&01&T&T&1&!1!&",
        # "https://hasilun.puspendik.kemdikbud.go.id/#2019!paketb!daya_serap!02&99&999!T&01&T&T&1&!3!&",
        ]

jenjangs = ["smp", "sma", "smk", "paketb", "paketc"]
#"smp", "sma", "smk", "paketb", "paketc"
tahuns = ["2019", "2018"]
prodis = ["b", "a", "s", "g", "k", "p"]
for jenjang in jenjangs:
    for tahun in tahuns:
        for i in range(1, 35):
            if i < 10:
                i = "0"+str(i)
            if jenjang == "sma":
                for prodi in prodis:
                    url = f'https://hasilun.puspendik.kemdikbud.go.id/#{tahun}!{jenjang}!daya_serap!{i}&99&999!{prodi}&01&1&T&1&!3!&'
                    links.append(url)
            elif jenjang == "paketc":
                for j in range(1, 3):
                    url = f'https://hasilun.puspendik.kemdikbud.go.id/#{tahun}!{jenjang}!daya_serap!{i}&99&999!{prodis[j]}&01&T&T&1&!1!&'
                    links.append(url)
            elif jenjang == "paketb":
                url = f'https://hasilun.puspendik.kemdikbud.go.id/#{tahun}!{jenjang}!daya_serap!{i}&99&999!T&01&T&T&1&!3!&'
                links.append(url)
            elif jenjang == "smp":
                url = f'https://hasilun.puspendik.kemdikbud.go.id/#{tahun}!{jenjang}!daya_serap!{i}&99&999!T&01&1&T&1&!3!&'
                links.append(url)

with ProcessPoolExecutor(max_workers=1) as executor:
    futures = [ executor.submit(get_nilai_materi, url) for url in links ]
    results = []
    for result in as_completed(futures):
        results.append(result)