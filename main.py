from myapp import MyApp

# Mengimpor kelas MyApp dari modul myapp.

if __name__ == "__main__":
   # Memastikan bahwa kode hanya dijalankan jika skrip ini dieksekusi langsung,
   # bukan saat diimpor sebagai modul oleh skrip lain.
   app = MyApp()
   # Membuat instance dari kelas MyApp.
   app.mainloop()
   # Memulai loop utama aplikasi. Metode mainloop() biasanya digunakan dalam aplikasi GUI
   # untuk menjalankan loop peristiwa yang terus-menerus sehingga aplikasi tetap berjalan dan responsif.
