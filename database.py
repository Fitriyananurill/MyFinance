import mysql.connector
# Mengimpor modul mysql.connector untuk menghubungkan dan berinteraksi dengan database MySQL.

cn = mysql.connector.connect(host="localhost", user="root", password="", database="pemvis")
# Membuat koneksi ke database MySQL dengan menentukan host (localhost), user (root), password (kosong), dan nama database (pemvis).

if cn.is_connected():
   # Memeriksa apakah koneksi ke database berhasil.
   print("Server database telah terhubung")
   # Jika koneksi berhasil, mencetak pesan "Server database telah terhubung".