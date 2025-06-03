from tkinter import messagebox
# Mengimpor messagebox dari modul tkinter untuk menampilkan pesan kesalahan atau informasi.

import customtkinter as ctk
# Mengimpor customtkinter sebagai ctk untuk membuat antarmuka GUI dengan tampilan yang disesuaikan.

from PIL import Image
# Mengimpor Image dari PIL (Python Imaging Library) untuk memproses gambar.

from database import cn
# Mengimpor objek cn dari modul database, yang berfungsi sebagai koneksi ke database.

from dashboard_tab import Dashboard
# Mengimpor kelas Dashboard dari modul dashboard_tab.

class LoginTab:
   def __init__(self, root):
       # Konstruktor kelas LoginTab yang menerima root sebagai parameter dan memanggil metode login.
       self.root = root
       self.login()

   def login(self):
       # Metode untuk mengatur tampilan tab login.

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

       sub_label = ctk.CTkLabel(right_frame, text="Silahkan masuk ke akunmu!", font=('Roboto', 15), text_color='grey', fg_color='white')
       sub_label.place(relx=0.15, rely=0.20, anchor="w")
       # Menambahkan sub-label instruksi pada frame kanan.

       entry_font = ('Helvetica', 10)
       entry_width = 30
       # Mendefinisikan font dan lebar entri untuk semua input.

       email_label = ctk.CTkLabel(right_frame, text="Email", font=('Roboto', 10), fg_color='white')
       email_label.place(relx=0.15, rely=0.28, anchor="w")
       self.email_entry = ctk.CTkEntry(right_frame, font=entry_font, width=entry_width * 10, height=30, corner_radius=10, border_color="black", fg_color='white')
       self.email_entry.place(relx=0.15, rely=0.33, anchor="w")
       # Menambahkan label dan entri untuk email.

       password_label = ctk.CTkLabel(right_frame, text="Password", font=('Roboto', 10), fg_color='white')
       password_label.place(relx=0.15, rely=0.38, anchor="w")
       self.password_entry = ctk.CTkEntry(right_frame, font=entry_font, width=entry_width * 10, height=30, corner_radius=10, border_color="black", fg_color='white', show="*")
       self.password_entry.place(relx=0.15, rely=0.43, anchor="w")
       # Menambahkan label dan entri untuk password dengan input tersembunyi.

       forget_password_label = ctk.CTkLabel(right_frame, text="Lupa Password?", font=('Helvetica', 10), text_color='red', fg_color='white', cursor="hand2")
       forget_password_label.place(relx=0.15, rely=0.48, anchor="w")
       forget_password_label.bind("<Button-1>", lambda e: self.updatepw())
       # Menambahkan label "Lupa Password?" dengan event binding untuk beralih ke tab update password.

       button_frame = ctk.CTkFrame(right_frame, fg_color='black')
       button_frame.place(relx=0.15, rely=0.55, anchor="w")
       # Membuat frame untuk menempatkan tombol.

       login_button = ctk.CTkButton(button_frame, text="Masuk", font=('Helvetica', 12, 'bold'), fg_color='#FECE8E', text_color='white', width=300, height=30, command=self.login_action)
       login_button.pack(padx=2, pady=2)
       # Menambahkan tombol login dan menghubungkannya ke metode login_action.

       img_path = "img1.PNG"
       img = Image.open(img_path)
       img = img.resize((500, 500), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))
       # Memuat dan mengubah ukuran gambar untuk ditampilkan di frame kiri.

       img_label = ctk.CTkLabel(left_frame, image=ctk_img, fg_color='#97D3CB', text="")
       img_label.place(relx=0.5, rely=0.5, anchor="center")
       # Menambahkan label gambar ke frame kiri.

       login_label = ctk.CTkLabel(right_frame, text="Belum Punya Akun? Daftar", font=('Helvetica', 10), text_color='red', fg_color='white', cursor="hand2")
       login_label.place(relx=0.35, rely=0.61, anchor="w")
       login_label.bind("<Button-1>", lambda e: self.signup())
       # Menambahkan label untuk pendaftaran dengan event binding untuk beralih ke tab pendaftaran.

   def login_action(self):
       # Metode untuk menangani aksi login pengguna.

       email = self.email_entry.get()
       password = self.password_entry.get()
       # Mengambil data dari entri email dan password.

       if not email or not password:
           messagebox.showerror("Error", "Email dan password harus diisi!")
           return
       # Memeriksa apakah email dan password telah diisi, jika tidak, menampilkan pesan kesalahan.

       cursor = cn.cursor()
       qry = "SELECT id, nama FROM data WHERE email = %s AND password = %s"
       val = (email, password)
       cursor.execute(qry, val)
       result = cursor.fetchone()
       # Mengeksekusi query untuk memeriksa apakah email dan password sesuai dengan data di database.

       if result:
           user_id, user_name = result
           messagebox.showinfo("Sukses", f"Login berhasil! Selamat datang, {user_name}")
           self.root.current_tab = Dashboard(self.root, user_id=user_id, user_name=user_name)
           self.root.current_tab.show_dashboard()
       else:
           messagebox.showerror("Error", "Email atau password salah!")
       # Jika login berhasil, menampilkan pesan sukses dan beralih ke dashboard.
       # Jika gagal, menampilkan pesan kesalahan.

   def signup(self):
       # Metode untuk beralih ke tab pendaftaran.

       from signup_tab import SignUpTab
       # Mengimpor SignUpTab dari modul signup_tab.

       for widget in self.root.winfo_children():
           widget.destroy()
       # Menghapus semua widget yang ada di dalam root.

       self.root.current_tab = SignUpTab(self.root)
       # Mengatur tab saat ini menjadi SignUpTab.

   def dashboard(self):
       # Metode untuk beralih ke dashboard.

       from dashboard_tab import Dashboard
       # Mengimpor Dashboard dari modul dashboard_tab.

       for widget in self.root.winfo_children():
           widget.destroy()
       # Menghapus semua widget yang ada di dalam root.

       self.root.current_tab = Dashboard(self.root)
       # Mengatur tab saat ini menjadi Dashboard.

   def updatepw(self):
       # Metode untuk beralih ke tab update password.

       from updatepw_tab import UpdatePWTab
       # Mengimpor UpdatePWTab dari modul updatepw_tab.

       for widget in self.root.winfo_children():
           widget.destroy()
       # Menghapus semua widget yang ada di dalam root.

       self.root.current_tab = UpdatePWTab(self.root)
       # Mengatur tab saat ini menjadi UpdatePWTab.