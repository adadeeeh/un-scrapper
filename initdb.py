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
drop_moda_ujian = """drop table moda_ujian"""
drop_relasi_sekolahmoda = """drop table relasi_sekolahmoda"""
drop_prodi = """drop table prodi"""

create_provinsi = """CREATE TABLE provinsi (
    id_prov int, nama_prov varchar(256), PRIMARY KEY (id_prov)
    );"""

create_kabupaten = """CREATE TABLE kota_kabupaten (
    id_kota int, id_prov int, nama_kota varchar(256), PRIMARY KEY (id_kota), FOREIGN KEY (id_prov) REFERENCES provinsi(id_prov)
    );"""

create_sekolah = """CREATE TABLE sekolah (
    id_sekolah int not null auto_increment, id_kota int, nama_sekolah varchar(256), jenjang_sekolah varchar(10), jenis_sekolah varchar(50), status_sekolah varchar(8),
    nosn varchar(256), PRIMARY KEY (id_sekolah), FOREIGN KEY (id_kota) REFERENCES kota_kabupaten(id_kota)
    );"""

create_moda_ujian = """create table moda_ujian (
    id_moda int not null auto_increment, jenis_ujian char(4), nama_moda varchar(256), primary key (id_moda))"""

create_relasi_sekolahmoda = """create table relasi_sekolahmoda (
	id_relasi int not null auto_increment, id_sekolah int, id_moda int, tahun_ajaran int,
    primary key (id_relasi, id_sekolah, id_moda), foreign key (id_sekolah) references sekolah(id_sekolah), foreign key (id_moda) references moda_ujian(id_moda));"""

create_prodi = """create table prodi (
    id_prodi int not null auto_increment, nama_prodi varchar(256), primary key (id_prodi))"""

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

def create_independent_db():
    db = pymysql.connect(host, user, password, dbname)
    cursor = db.cursor()

    try:
        cursor.execute(set_0)
        cursor.execute(drop_moda_ujian)
        cursor.execute(drop_prodi)
        cursor.execute(set_1)
        cursor.execute(create_moda_ujian)
        cursor.execute(create_prodi)
    except:
        cursor.execute(create_moda_ujian)
        cursor.execute(create_prodi)

def create_sekolah_db():
    db = pymysql.connect(host, user, password, dbname)
    cursor = db.cursor()

    try:
        cursor.execute(set_0)
        cursor.execute(drop_sekolah)
        cursor.execute(drop_relasi_sekolahmoda)
        cursor.execute(set_1)
        cursor.execute(create_sekolah)
        cursor.execute(create_relasi_sekolahmoda)
    except:
        cursor.execute(create_sekolah)
        cursor.execute(create_relasi_sekolahmoda)