import initdb

db = initdb.get_db()
cursor = initdb.get_cursor(db)

def provinsi(data):
    insert_query = """insert into provinsi(id_prov, nama_prov) values(%s, %s)"""
    cursor.execute(insert_query, data)
    db.commit()

def kabupaten(data):
    insert_query = """insert into kota_kabupaten(id_kota, id_prov, nama_kota) values(%s, %s, %s)"""
    cursor.execute(insert_query, data)
    db.commit()

def moda_ujian(data):
    insert_query = """insert into moda_ujian(jenis_ujian, nama_moda) values(%s, %s)"""
    cursor.execute(insert_query, data)
    db.commit()

def prodi(data):
    insert_query = """insert into prodi(nama_prodi) values(%s)"""
    cursor.execute(insert_query, data)
    db.commit()

def matuji(data):
    insert_query = """insert into mata_ujian(nama_matuji) values(%s)"""
    cursor.execute(insert_query, data)
    db.commit()

def get_id_prodi(nama_prodi):
    query = """select id_prodi from prodi where nama_prodi=%s"""
    cursor.execute(query, nama_prodi)
    result = cursor.fetchone()
    return result[0]

def get_id_matuji(nama_matuji):
    query = """select id_matuji from mata_ujian where nama_matuji=%s"""
    cursor.execute(query, nama_matuji)
    result = cursor.fetchone()
    return result[0]

def prodi_matuji(data):
    insert_query = "insert into prodi_punya_matuji(id_prodi, id_matuji, tahun_prodmat) values(%s, %s, %s)"
    cursor.execute(insert_query, data)
    db.commit()

def materi_ujian(data):
    insert_query = "insert into materi_ujian(id_matuji, materi) values(%s, %s)"
    cursor.execute(insert_query, data)
    db.commit()

def get_id_matuji_from_materi(data):
    insert_query = """select id_matuji from materi_ujian where materi=%s"""
    cursor.execute(insert_query, data)
    result = cursor.fetchall()
    if result == ():
        return result
    else:
        return result

# insert_query = """select id_matuji from materi_ujian where materi=%s"""
# cursor.execute(insert_query, 'MEMBACA NONSASTRA')
# result = cursor.fetchall()
# if result == ():
#     print(result)
# else:
#     print(result)

# for item in result:
#     print(item[0])

def get_id_materi(materi):
    query = """select id_materi from materi_ujian where materi=%s"""
    cursor.execute(query, materi)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        pass

def indikator_materi(data):
    insert_query = "insert into indikator_materi(id_materi, indikator) values(%s, %s)"
    cursor.execute(insert_query, data)
    db.commit()

def get_id_materi_by_indikator(data):
    insert_query = """select id_materi from indikator_materi where indikator=%s"""
    cursor.execute(insert_query, data)
    result = cursor.fetchall()
    if result == ():
        return result
    else:
        return result

# insert_query = """select id_materi from indikator_materi where indikator=%s"""
# cursor.execute(insert_query, "Melengkapi dialog dengan tepat")
# result = cursor.fetchall()
# if result == ():
#     print(result)
# else:
#     print(result)

# for item in result:
#     print(item[0])

def get_id_indikator(data):
    query = """select id_indikator from indikator_materi where indikator=%s"""
    cursor.execute(query, data)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        pass

def relasi_matindor(data):
    insert_query = "insert into relasi_matindor(id_materi, id_prodi, id_indikator, id_matuji, urutan_indikator, tahun_indikator) values(%s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, data)
    db.commit()

def get_id_moda(data):
    query = """select id_moda from moda_ujian where jenis_ujian=%s"""
    cursor.execute(query, data)
    result = cursor.fetchone()
    return result[0]

def sekolah(data):
    insert_query = """insert into sekolah(id_sekolah, id_kota, nama_sekolah, jenjang_sekolah, jenis_sekolah, status_sekolah, npsn)
                    values(%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(insert_query, data)
    db.commit()

def get_id_sekolah(data):
    query = """select id_sekolah from sekolah where nama_sekolah=%s"""
    cursor.execute(query, data)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        pass

def relasi_sekolah_moda(data):
    insert_query = "insert into relasi_sekolahmoda(id_sekolah, id_moda, tahun_ajaran) values(%s, %s, %s)"
    cursor.execute(insert_query, data)
    db.commit()

def get_id_relasi_sekolah_moda(data):
    query = """select id_sekolah from relasi_sekolahmoda where id_sekolah=%s and id_moda=%s and tahun_ajaran=%s"""
    cursor.execute(query, data)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        pass

def relasi_sekolah_memiliki_prodi(data):
    insert_query = "insert into sekolah_memiliki_prodi(id_sekolah, id_prodi, jumlah_siswa, tahun_jumlahsiswa) values(%s, %s, %s, %s)"
    cursor.execute(insert_query, data)
    db.commit()

def get_id_relasi_sekolah_prodi(data):
    query = """select id_sekolah from sekolah_memiliki_prodi where id_sekolah=%s and id_prodi=%s and jumlah_siswa=%s and tahun_jumlahsiswa=%s"""
    cursor.execute(query, data)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        pass

def nilai_matuji(data):
    insert_query = "insert into nilai_matuji(id_matuji, id_prodi, id_sekolah, avg_matuji, tahun_avgmatuji) values(%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, data)
    db.commit()

def get_id_nilai_matuji(data):
    query = """select id_relasiavgmatuji from nilai_matuji where id_matuji=%s and id_prodi=%s and id_sekolah=%s and avg_matuji=%s and tahun_avgmatuji=%s"""
    cursor.execute(query, data)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        pass

def soal_rilis(data):
    insert_query = "insert into soal_rilis(tahun, link, judul) values(%s, %s, %s)"
    cursor.execute(insert_query, data)
    db.commit()

def get_id_provinsi(data):
    query = """select id_prov from provinsi where nama_prov=%s"""
    cursor.execute(query, data)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        pass

def infografis(data):
    insert_query = "insert into infografis_wilayah(id_prov, tahun, jenjang_sekolah, jenis, link) values(%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, data)
    db.commit()

def nilai_materi(data):
    insert_query = "insert into nilai_materi(id_materi, id_matuji, id_prodi, id_sekolah, avg_materi, tahun_avgmateri) values(%s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, data)
    db.commit()

def get_id_nilai_materi(data):
    query = """select id_relasiavgmateri from nilai_materi where id_materi=%s and id_matuji=%s and id_prodi=%s and id_sekolah=%s and avg_materi=%s and tahun_avgmateri=%s"""
    cursor.execute(query, data)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        pass

def nilai_indikator(data):
    insert_query = "insert into nilai_indikator(id_indikator, id_matuji, id_materi, id_prodi, id_sekolah, avg_indikator, tahun_avgindikator) values(%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, data)
    db.commit()

def get_id_nilai_indikator(data):
    query = """select id_relasiavgindi from nilai_indikator where id_indikator=%s and id_matuji=%s and id_materi=%s and id_prodi=%s and id_sekolah=%s and avg_indikator=%s and tahun_avgindikator=%s"""
    cursor.execute(query, data)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        pass