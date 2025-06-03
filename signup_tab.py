from tkinter import messagebox
# Mengimpor messagebox dari modul tkinter untuk menampilkan pesan kesalahan atau informasi.

import customtkinter as ctk
# Mengimpor customtkinter sebagai ctk untuk membuat antarmuka GUI dengan tampilan yang disesuaikan.

from PIL import Image
# Mengimpor Image dari PIL (Python Imaging Library) untuk memproses gambar.

from database import cn
# Mengimpor objek cn dari modul database, yang berfungsi sebagai koneksi ke database.

class SignUpTab:
   def __init__(self, root):
       # Konstruktor kelas SignUpTab yang menerima root sebagai parameter dan memanggil metode signup.
       self.root = root
       self.signup()

   def signup(self):
       # Metode untuk mengatur tampilan tab pendaftaran.

       for widget in self.root.winfo_children():
           widget.destroy()
       # Menghapus semua widget yang ada di dalam root.

       left_frame = ctk.CTkFrame(self.root, width=550, height=600, fg_color='#97D3CB', corner_radius=0)
       left_frame.grid(row=0, column=0, sticky="nsew")
       # Membuat frame kiri dengan latar belakang hijau dan menempatkannya di grid.

       right_frame = ctk.CTkFrame(self.root, width=450, height=600, fg_color='white')
       right_frame.grid(row=0, column=1, sticky="nsew")
       # Membuat frame kanan dengan latar belakang putih dan menempatkannya di grid.

       welcome_label = ctk.CTkLabel(right_frame, text="Selamat Datang", font=('Roboto', 20), fg_color='white')
       welcome_label.place(relx=0.15, rely=0.15, anchor="w")
       # Menambahkan label selamat datang pada frame kanan.

       sub_label = ctk.CTkLabel(right_frame, text="Isi data berikut untuk pendaftaran akun barumu!", font=('Roboto', 15), text_color='grey', fg_color='white')
       sub_label.place(relx=0.15, rely=0.20, anchor="w")
       # Menambahkan sub-label instruksi pada frame kanan.

       entry_font = ('Helvetica', 10)
       entry_width = 30
       # Mendefinisikan font dan lebar entri untuk semua input.

       nama_label = ctk.CTkLabel(right_frame, text="Nama", font=('Roboto', 10), fg_color='white')
       nama_label.place(relx=0.15, rely=0.28, anchor="w")
       self.nama_entry = ctk.CTkEntry(right_frame, font=entry_font, width=entry_width * 10, height=30, corner_radius=10, border_color="black", fg_color='white')
       self.nama_entry.place(relx=0.15, rely=0.33, anchor="w")
       # Menambahkan label dan entri untuk nama.

       telepon_label = ctk.CTkLabel(right_frame, text="Nomor Telepon", font=('Roboto', 10), fg_color='white')
       telepon_label.place(relx=0.15, rely=0.38, anchor="w")
       self.telepon_entry = ctk.CTkEntry(right_frame, font=entry_font, width=entry_width * 10, height=30, corner_radius=10, border_color="black", fg_color='white')
       self.telepon_entry.place(relx=0.15, rely=0.43, anchor="w")
       # Menambahkan label dan entri untuk nomor telepon.

       email_label = ctk.CTkLabel(right_frame, text="Email", font=('Roboto', 10), fg_color='white')
       email_label.place(relx=0.15, rely=0.48, anchor="w")
       self.email_entry = ctk.CTkEntry(right_frame, font=entry_font, width=entry_width * 10, height=30, corner_radius=10, border_color="black", fg_color='white')
       self.email_entry.place(relx=0.15, rely=0.53, anchor="w")
       # Menambahkan label dan entri untuk email.

       password_label = ctk.CTkLabel(right_frame, text="Password", font=('Roboto', 10), fg_color='white')
       password_label.place(relx=0.15, rely=0.58, anchor="w")
       self.password_entry = ctk.CTkEntry(right_frame, font=entry_font, width=entry_width * 10, height=30, corner_radius=10, border_color="black", fg_color='white', show="*")
       self.password_entry.place(relx=0.15, rely=0.63, anchor="w")
       # Menambahkan label dan entri untuk password dengan input tersembunyi.

       button_frame = ctk.CTkFrame(right_frame, fg_color='black')
       button_frame.place(relx=0.15, rely=0.72, anchor="w")
       # Membuat frame untuk menempatkan tombol.

       register_button = ctk.CTkButton(button_frame, text="Daftar", font=('Helvetica', 12, 'bold'), fg_color='#FECE8E', text_color='white', width=300, height=30, command=self.register)
       register_button.pack(padx=2, pady=2)
       # Menambahkan tombol daftar dan menghubungkannya ke metode register.

       img_path = "img1.PNG"
       img = Image.open(img_path)
       img = img.resize((500, 500), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))
       # Memuat dan mengubah ukuran gambar untuk ditampilkan di frame kiri.

       img_label = ctk.CTkLabel(left_frame, image=ctk_img, fg_color='#97D3CB', text="")
       img_label.place(relx=0.5, rely=0.5, anchor="center")
       # Menambahkan label gambar ke frame kiri.

       login_label = ctk.CTkLabel(right_frame, text="Sudah Punya Akun? Masuk", font=('Helvetica', 10), text_color='red', fg_color='white', cursor="hand2")
       login_label.place(relx=0.35, rely=0.79, anchor="w")
       login_label.bind("<Button-1>", lambda e: self.login())
       # Menambahkan label untuk login dengan event binding untuk beralih ke tab login.

   def register(self):
       # Metode untuk menangani pendaftaran pengguna baru.

       nama = self.nama_entry.get()
       telepon = self.telepon_entry.get()
       email = self.email_entry.get()
       password = self.password_entry.get()
       # Mengambil data dari entri.

       if not nama or not telepon or not email or not password:
           return messagebox.showerror("Error", "Semua kolom harus diisi!")
       # Memeriksa apakah semua entri telah diisi, jika tidak, menampilkan pesan kesalahan.

       cursor = cn.cursor()
       qry = "INSERT INTO data (nama, telepon, email, password) VALUES (%s, %s, %s, %s)"
       val = (nama, telepon, email, password)
       cursor.execute(qry, val)
       cn.commit()
       # Menambahkan data pengguna baru ke database.

       messagebox.showinfo("Sukses", "Pendaftaran berhasil!")
       # Menampilkan pesan sukses setelah pendaftaran berhasil.

       self.nama_entry.delete(0, 'end')
       self.telepon_entry.delete(0, 'end')
       self.email_entry.delete(0, 'end')
       self.password_entry.delete(0, 'end')
       # Mengosongkan entri setelah pendaftaran.

       self.login()
       # Beralih ke tab login setelah pendaftaran berhasil.

   def login(self):
       from login_tab import LoginTab
       # Mengimpor LoginTab dari modul login_tab.

       for widget in self.root.winfo_children():
           widget.destroy()
       # Menghapus semua widget yang ada di dalam root.

       self.root.current_tab = LoginTab(self.root)
       # Mengatur tab saat ini menjadi LoginTab.