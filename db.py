import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123",
        database="gudang_db"
    )

def insert_kategori(nama_kategori):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO kategori (nama_kategori) VALUES (%s)", (nama_kategori,))
    conn.commit()
    conn.close()

def update_kategori(id, nama_kategori):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE kategori SET nama_kategori = %s WHERE id = %s", (nama_kategori, id))
    conn.commit()
    conn.close()

def delete_kategori(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM kategori WHERE id = %s", (id,))
    conn.commit()
    conn.close()
