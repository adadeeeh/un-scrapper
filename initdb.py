import pymysql

host = 'localhost'
user = 'pedro'
password = '1'
dbname = 'crawl'

set_0 = """SET FOREIGN_KEY_CHECKS=0"""
set_1 = """SET FOREIGN_KEY_CHECKS=1"""
drop_provinsi = """DROP TABLE provinsi"""
drop_kabupaten = """DROP TABLE kota_kabupaten"""
drop_sekolah = """DROP TABLE sekolah"""

create_provinsi = """CREATE TABLE provinsi (
    id_prov int, nama_prov varchar(256), PRIMARY KEY (id_prov)
    );"""

create_kabupaten = """CREATE TABLE kota_kabupaten (
    id_kota int, id_prov int, PRIMARY KEY (id_kota), FOREIGN KEY (id_prov) REFERENCES provinsi(id_prov)
    );"""

create_sekolah = """CREATE TABLE sekolah (
    id_sekolah int not null auto_increment, id_kota int, nama_sekolah varchar(256), jenjang_sekolah varchar(10), jenis_sekolah varchar(50), status_sekolah varchar(8),
    nosn varchar(256), PRIMARY KEY (id_sekolah), FOREIGN KEY (id_kota) REFERENCES kota_kabupaten(id_kota)
    );"""

def get_cursor(db):
    return db.cursor()

def get_db():
    db = pymysql.connect(host, user, password, dbname)
    return db

def create_prov_kab_db():
    db = pymysql.connect(host, user, password, dbname)
    cursor = db.cursor()

    try:
        cursor.execute(set_0)
        cursor.execute(drop_provinsi)
        cursor.execute(drop_kabupaten)
        cursor.execute(set_1)
        cursor.execute(create_provinsi)
        cursor.execute(create_kabupaten)
    except:
        cursor.execute(create_provinsi)
        cursor.execute(create_kabupaten)

def create_sekolah_db():
    db = pymysql.connect(host, user, password, dbname)
    cursor = db.cursor()

    try:
        cursor.execute(set_0)
        cursor.execute(drop_sekolah)
        cursor.execute(set_1)
        cursor.execute(create_sekolah)
    except:
        cursor.execute(create_sekolah)