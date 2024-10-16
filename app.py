import streamlit as st
import pandas as pd
from db import get_db_connection, insert_kategori, update_kategori, delete_kategori

def get_data(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fungsi untuk reload data kategori
def reload_kategori_data():
    st.session_state["kategori_data"] = get_data("SELECT * FROM kategori")

# Memastikan data kategori hanya di-load sekali dan disimpan dalam session_state
if "kategori_data" not in st.session_state:
    reload_kategori_data()

# Fungsi untuk menangani perubahan data
def on_submit_kategori():
    insert_kategori(st.session_state["new_kategori_name"])
    st.success("Kategori berhasil ditambahkan!")
    reload_kategori_data()

def on_edit_kategori():
    kategori_id = st.session_state["kategori_list"].loc[
        st.session_state["kategori_list"]['nama_kategori'] == st.session_state["kategori_edit"], 'id'
    ].values[0]
    update_kategori(kategori_id, st.session_state["new_nama_kategori"])
    st.success("Kategori berhasil diperbarui!")
    reload_kategori_data()

def on_delete_kategori():
    kategori_id = st.session_state["kategori_list"].loc[
        st.session_state["kategori_list"]['nama_kategori'] == st.session_state["kategori_hapus"], 'id'
    ].values[0]
    delete_kategori(kategori_id)
    st.success("Kategori berhasil dihapus!")
    reload_kategori_data()

# Tab untuk Kategori
tab1, tab2, tab3, tab4 = st.tabs(["Barang", "Barang Masuk", "Barang Keluar", "Kategori"])

with tab4:
    st.header("Manajemen Kategori")

    # Tampilkan data kategori
    st.dataframe(st.session_state["kategori_data"])

    # Form Tambah Kategori
    with st.form("Tambah Kategori", clear_on_submit=True):
        st.text_input("Nama Kategori", key="new_kategori_name")
        submit_kategori = st.form_submit_button("Tambah Kategori", on_click=on_submit_kategori)

    # Form Edit Kategori
    st.session_state["kategori_list"] = get_data("SELECT * FROM kategori")
    with st.form("Edit Kategori"):
        st.selectbox("Pilih Kategori", st.session_state["kategori_list"]['nama_kategori'], key="kategori_edit")
        st.text_input("Nama Baru Kategori", key="new_nama_kategori")
        submit_edit = st.form_submit_button("Edit Kategori", on_click=on_edit_kategori)

    # Form Hapus Kategori
    with st.form("Hapus Kategori"):
        st.selectbox("Pilih Kategori untuk Dihapus", st.session_state["kategori_list"]['nama_kategori'], key="kategori_hapus")
        submit_hapus = st.form_submit_button("Hapus Kategori", on_click=on_delete_kategori)


with tab1:
    st.header("Data Barang")
    barang = get_data(
    """
    SELECT 
        barang.id AS barang_id, 
        barang.nama_barang, 
        barang.kategori_id, 
        barang.stok, 
        kategori.id AS kategori_id, 
        kategori.nama_kategori 
    FROM barang 
    JOIN kategori ON barang.kategori_id = kategori.id
    """
)
    st.dataframe(barang[['barang_id', 'nama_barang', 'nama_kategori', 'stok']])

    with st.form("Tambah Barang"):
        nama = st.text_input("Nama Barang")
        kategori_list = get_data("SELECT * FROM kategori")
        kategori = st.selectbox("Kategori", kategori_list['nama_kategori'])
        stok = st.number_input("Stok Awal", min_value=0, step=1)
        submit = st.form_submit_button("Tambah Barang")

        if submit:
            kategori_id = kategori_list.loc[kategori_list['nama_kategori'] == kategori, 'id'].values[0]
            insert_barang(nama, int(kategori_id), stok)
            st.success("Barang berhasil ditambahkan!")
            st.experimental_rerun()  # Refresh halaman

with tab2:
    st.header("Barang Masuk")
    barang_masuk = get_data(
        "SELECT barang_masuk.*, barang.nama_barang, supplier.nama_supplier FROM barang_masuk "
        "JOIN barang ON barang_masuk.barang_id = barang.id "
        "JOIN supplier ON barang_masuk.supplier_id = supplier.id"
    )
    st.dataframe(barang_masuk)

    with st.form("Tambah Barang Masuk"):
        barang_list = get_data("SELECT * FROM barang")
        barang = st.selectbox("Barang", barang_list['nama_barang'])
        supplier_list = get_data("SELECT * FROM supplier")
        supplier = st.selectbox("Supplier", supplier_list['nama_supplier'])
        jumlah = st.number_input("Jumlah", min_value=1, step=1)
        tanggal = st.date_input("Tanggal Masuk")
        submit_masuk = st.form_submit_button("Tambah Barang Masuk")

        if submit_masuk:
            barang_id = barang_list.loc[barang_list['nama_barang'] == barang, 'id'].values[0]
            supplier_id = supplier_list.loc[supplier_list['nama_supplier'] == supplier, 'id'].values[0]
            insert_barang_masuk(barang_id, supplier_id, jumlah, tanggal)
            update_stok(barang_id, jumlah, is_masuk=True)
            st.success("Barang masuk berhasil ditambahkan!")
            st.experimental_rerun()  # Refresh halaman

with tab3:
    st.header("Barang Keluar")
    barang_keluar = get_data(
        "SELECT barang_keluar.*, barang.nama_barang, pelanggan.nama_pelanggan FROM barang_keluar "
        "JOIN barang ON barang_keluar.barang_id = barang.id "
        "JOIN pelanggan ON barang_keluar.pelanggan_id = pelanggan.id"
    )
    st.dataframe(barang_keluar)

    with st.form("Tambah Barang Keluar"):
        barang_list = get_data("SELECT * FROM barang")
        barang = st.selectbox("Barang", barang_list['nama_barang'])
        pelanggan_list = get_data("SELECT * FROM pelanggan")
        pelanggan = st.selectbox("Pelanggan", pelanggan_list['nama_pelanggan'])
        jumlah = st.number_input("Jumlah", min_value=1, step=1)
        tanggal = st.date_input("Tanggal Keluar")
        submit_keluar = st.form_submit_button("Tambah Barang Keluar")

        if submit_keluar:
            barang_id = barang_list.loc[barang_list['nama_barang'] == barang, 'id'].values[0]
            pelanggan_id = pelanggan_list.loc[pelanggan_list['nama_pelanggan'] == pelanggan, 'id'].values[0]
            update_stok(barang_id, jumlah, is_masuk=False)
            st.success("Barang keluar berhasil ditambahkan!")
            st.experimental_rerun()  # Refresh halaman