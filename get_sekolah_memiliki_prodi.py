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



links = [
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&99&999!T&T&T&T&1&unbk!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smp!capaian!01&99&999!T&T&T&T&1&unkp!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!capaian!01&99&999!b&T&T&T&1&unbk!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!sma!capaian!01&99&999!b&T&T&T&1&unkp!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smk!capaian!01&99&999!T&T&1&T&1&unbk!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!smk!capaian!01&99&999!T&T&1&T&1&unkp!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!paketb!capaian!01&99&999!T&T&T&T&1&!3!&",
            # "https://hasilun.puspendik.kemdikbud.go.id/#2019!paketc!capaian!01&99&999!T&T&T&T&1&!3!&"
        ]

jenjangs = ["smp", "sma", "smk", "paketb", "paketc"]
modas = ["unbk", "unkp"]
tahuns = ["2019", "2018"]
for jenjang in jenjangs:
    for moda in modas:
        for tahun in tahuns:
            for i in range(1, 35):
                if i < 10:
                    i = "0"+str(i)
                if jenjang == "paketb" or jenjang == "paketc":
                    moda = "1"
                url = f'https://hasilun.puspendik.kemdikbud.go.id/#{tahun}!{jenjang}!capaian!{i}&99&999!T&T&1&T&1&{moda}!3!&'
                # links.append(url)

with ProcessPoolExecutor(max_workers=1) as executor:
    futures = [ executor.submit(get_relasi, url) for url in links ]
    results = []
    for result in as_completed(futures):
        results.append(result)