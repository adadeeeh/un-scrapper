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