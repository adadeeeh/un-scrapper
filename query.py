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