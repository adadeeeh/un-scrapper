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
drop_matuji = """drop table mata_ujian"""
drop_prodi_matuji = """drop table prodi_punya_matuji"""
drop_materi_ujian = """drop table materi_ujian"""
drop_indikator_materi = """drop table indikator_materi"""
drop_relasi_matindor = "drop table relasi_matindor"
drop_sekolah_memiliki_prodi = "drop table sekolah_memiliki_prodi"
drop_nilai_matuji = "drop table nilai_matuji"

create_provinsi = """CREATE TABLE provinsi (
    id_prov int, nama_prov varchar(256), PRIMARY KEY (id_prov)
    );"""

create_kabupaten = """CREATE TABLE kota_kabupaten (
    id_kota varchar(256), id_prov int, nama_kota varchar(256), PRIMARY KEY (id_kota), FOREIGN KEY (id_prov) REFERENCES provinsi(id_prov)
    );"""

create_sekolah = """CREATE TABLE sekolah (
    id_sekolah varchar(256) not null, id_kota int, nama_sekolah varchar(256), jenjang_sekolah varchar(10), jenis_sekolah varchar(50), status_sekolah varchar(8),
    npsn varchar(256), PRIMARY KEY (id_sekolah), FOREIGN KEY (id_kota) REFERENCES kota_kabupaten(id_kota)
    );"""

create_moda_ujian = """create table moda_ujian (
    id_moda int not null auto_increment, jenis_ujian char(4), nama_moda varchar(256), primary key (id_moda))"""

create_relasi_sekolahmoda = """create table relasi_sekolahmoda (
	id_relasi int not null auto_increment, id_sekolah varchar(256), id_moda int, tahun_ajaran int,
    primary key (id_relasi, id_sekolah, id_moda), foreign key (id_sekolah) references sekolah(id_sekolah), foreign key (id_moda) references moda_ujian(id_moda));"""

create_prodi = """create table prodi (
    id_prodi int not null auto_increment, nama_prodi varchar(256), primary key (id_prodi))"""

create_matuji = """create table mata_ujian (
    id_matuji int not null auto_increment, nama_matuji varchar(256), primary key (id_matuji))"""

create_prodi_matuji = """create table prodi_punya_matuji (
    id_relasiprodmat int not null auto_increment, id_prodi int, id_matuji int, tahun_prodmat int, primary key (id_relasiprodmat), foreign key (id_prodi) references prodi(id_prodi),
    foreign key (id_matuji) references mata_ujian(id_matuji))"""

create_materi_ujian = """create table materi_ujian (
    id_materi int not null auto_increment, id_matuji int, materi varchar(256), primary key (id_materi), foreign key (id_matuji) references mata_ujian(id_matuji))"""

create_indikator_materi = """create table indikator_materi (
    id_indikator int not null auto_increment, id_materi int, indikator long varchar, primary key (id_indikator), foreign key (id_materi) references materi_ujian(id_materi))"""

create_relasi_matindor = """create table relasi_matindor (
    id_relasimatindor int not null auto_increment, id_materi int, id_prodi int, id_indikator int, id_matuji int, urutan_indikator numeric, tahun_indikator int,
    primary key (id_relasimatindor), foreign key (id_materi) references materi_ujian(id_materi), foreign key (id_prodi) references prodi(id_prodi),
    foreign key (id_indikator) references indikator_materi(id_indikator), foreign key (id_matuji) references mata_ujian(id_matuji));"""

create_sekolah_memiliki_prodi = """create table sekolah_memiliki_prodi (
    id_relasisekolahprodi int not null auto_increment, id_sekolah varchar(256), id_prodi int, jumlah_siswa int, tahun_jumlahsiswa int, primary key (id_relasisekolahprodi, id_sekolah, id_prodi),
    foreign key (id_sekolah) references sekolah(id_sekolah), foreign key (id_prodi) references prodi(id_prodi));"""

create_nilai_matuji = """create table nilai_matuji (
    id_relasiavgmatuji int not null auto_increment, id_matuji int, id_prodi int, id_sekolah varchar(256), avg_matuji varchar(10), tahun_avgmatuji int,
    primary key (id_relasiavgmatuji, id_matuji, id_prodi, id_sekolah), foreign key (id_matuji) references mata_ujian(id_matuji), foreign key (id_prodi) references prodi(id_prodi),
    foreign key (id_sekolah) references sekolah(id_sekolah))"""

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
        cursor.execute(drop_matuji)
        cursor.execute(set_1)
        cursor.execute(create_moda_ujian)
        cursor.execute(create_prodi)
        cursor.execute(create_matuji)
    except:
        cursor.execute(create_moda_ujian)
        cursor.execute(create_prodi)
        cursor.execute(create_matuji)

def create_prodi_matuji_db():
    db = pymysql.connect(host, user, password, dbname)
    cursor = db.cursor()

    try:
        cursor.execute(set_0)
        cursor.execute(drop_prodi_matuji)
        cursor.execute(set_1)
        cursor.execute(create_prodi_matuji)
    except:
        cursor.execute(create_prodi_matuji)

def create_materi_ujian_db():
    db = pymysql.connect(host, user, password, dbname)
    cursor = db.cursor()

    try:
        cursor.execute(set_0)
        cursor.execute(drop_materi_ujian)
        cursor.execute(set_1)
        cursor.execute(create_materi_ujian)
    except:
        cursor.execute(create_materi_ujian)

def create_indikator_db():
    db = pymysql.connect(host, user, password, dbname)
    cursor = db.cursor()

    try:
        cursor.execute(set_0)
        cursor.execute(drop_indikator_materi)
        cursor.execute(set_1)
        cursor.execute(create_indikator_materi)
    except:
        cursor.execute(create_indikator_materi)

def create_relasi_matindor_db():
    db = pymysql.connect(host, user, password, dbname)
    cursor = db.cursor()

    try:
        cursor.execute(set_0)
        cursor.execute(drop_relasi_matindor)
        cursor.execute(set_1)
        cursor.execute(create_relasi_matindor)
    except:
        cursor.execute(create_relasi_matindor)

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

def create_relasi_sekolah_moda_db():
    db = pymysql.connect(host, user, password, dbname)
    cursor = db.cursor()

    try:
        cursor.execute(set_0)
        cursor.execute(drop_relasi_sekolahmoda)
        cursor.execute(set_1)
        cursor.execute(create_relasi_sekolahmoda)
    except:
        cursor.execute(create_relasi_sekolahmoda)

def create_sekolah_memiliki_prodi_db():
    db = pymysql.connect(host, user, password, dbname)
    cursor = db.cursor()

    try:
        cursor.execute(set_0)
        cursor.execute(drop_sekolah_memiliki_prodi)
        cursor.execute(set_1)
        cursor.execute(create_sekolah_memiliki_prodi)
    except:
        cursor.execute(create_sekolah_memiliki_prodi)

def create_nilai_matuji_db():
    db = pymysql.connect(host, user, password, dbname)
    cursor = db.cursor()

    try:
        cursor.execute(set_0)
        cursor.execute(drop_nilai_matuji)
        cursor.execute(set_1)
        cursor.execute(create_nilai_matuji)
    except:
        cursor.execute(create_nilai_matuji)