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
    return result[0]

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
    return result[0]

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