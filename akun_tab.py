import customtkinter as ctk  # Mengimpor modul customtkinter dengan alias ctk
from PIL import Image  # Mengimpor modul Image dari PIL
from tkinter import filedialog, messagebox  # Mengimpor fungsi filedialog dan messagebox dari modul tkinter
from database import cn  # Mengimpor koneksi database dari modul database

class Akun:
   def __init__(self, root, user_id, user_name):
       self.root = root  # Menyimpan root tkinter sebagai atribut self.root
       self.root.geometry("1000x600")  # Mengatur ukuran jendela utama
       self.current_user_id = user_id  # Menyimpan user_id saat ini sebagai atribut self.current_user_id
       self.user_name = user_name  # Menyimpan user_name sebagai atribut self.user_name
       self.show_Akun()  # Memanggil metode show_Akun() untuk menampilkan halaman Akun

   def show_Akun(self):
       for widget in self.root.winfo_children():
           widget.destroy()  # Menghapus semua widget yang ada di dalam root tkinter
       self.root.grid_rowconfigure(0, weight=1)  # Mengatur konfigurasi baris grid pada root tkinter
       self.root.grid_columnconfigure(0, weight=1)  # Mengatur konfigurasi kolom grid pada root tkinter

       def show_dashboard_page(event=None):
           self.show_dashboard()  # Metode untuk menampilkan halaman dashboard

       def show_pencatatan_page(event=None):
           self.show_Pencatatan()  # Metode untuk menampilkan halaman pencatatan

       def show_info_page(event=None):
           self.show_Info()  # Metode untuk menampilkan halaman info

       def show_akun_page(event=None):
           self.show_Akun()  # Metode untuk menampilkan halaman akun (self-referential)

       container_frame = ctk.CTkFrame(self.root, fg_color='white', corner_radius=0)  # Membuat frame utama dengan modul customtkinter
       container_frame.grid(row=0, column=0, sticky="nsew")  # Meletakkan frame utama di grid tkinter

       container_frame.grid_rowconfigure(1, weight=1)  # Mengatur konfigurasi baris grid pada frame utama
       container_frame.grid_columnconfigure(1, weight=1)  # Mengatur konfigurasi kolom grid pada frame utama

       left_frame = ctk.CTkFrame(container_frame, width=60, height=600, fg_color='white', corner_radius=0)  # Membuat frame kiri dengan modul customtkinter
       left_frame.grid(row=1, column=0, sticky="nsew")  # Meletakkan frame kiri di grid tkinter

       top_frame = ctk.CTkFrame(container_frame, height=50, fg_color='white', corner_radius=0)  # Membuat frame atas dengan modul customtkinter
       top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")  # Meletakkan frame atas di grid tkinter

       # Menyiapkan gambar dan label untuk logo aplikasi
       img_path = "img1.PNG"
       img = Image.open(img_path)
       img = img.resize((50, 50), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(48, 48))
       img_label = ctk.CTkLabel(top_frame, image=ctk_img, text="")
       img_label.place(relx=0.005, rely=0.12)

       # Menampilkan teks judul aplikasi
       text_label = ctk.CTkLabel(top_frame, text="MY FINANCE", font=("Arial", 16, 'bold'), text_color='orange')
       text_label.place(relx=0.06, rely=0.20)

       # Menyiapkan gambar dan label untuk menu dashboard
       img_path = "img3.PNG"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(38, 38))
       img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
       img_label.place(relx=0.18, rely=0.35)
       text_label = ctk.CTkLabel(left_frame, text="Dashboard", font=("Arial", 8), text_color='gray')
       text_label.place(relx=0.15, rely=0.41)
       img_label.bind("<Button-1>", show_dashboard_page)  # Memasang event handler untuk menampilkan halaman dashboard

       # Menyiapkan gambar dan label untuk menu pencatatan
       img_path = "img4.PNG"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(33, 33))
       img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
       img_label.place(relx=0.30, rely=0.47)
       text_label = ctk.CTkLabel(left_frame, text="Pencatatan", font=("Arial", 8), text_color='gray')
       text_label.place(relx=0.15, rely=0.53)
       img_label.bind("<Button-1>", show_pencatatan_page)  # Memasang event handler untuk menampilkan halaman pencatatan

       # Menyiapkan gambar dan label untuk menu info
       img_path = "img6.png"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
       img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
       img_label.place(relx=0.14, rely=0.88)
       text_label = ctk.CTkLabel(left_frame, text="Info", font=("Arial", 8), text_color='gray')
       text_label.place(relx=0.38, rely=0.94)
       img_label.bind("<Button-1>", show_info_page)  # Memasang event handler untuk menampilkan halaman info

       # Menyiapkan gambar dan label untuk pesan sapaan pengguna
       img_path = "img5.png"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(35, 35))
       img_label = ctk.CTkLabel(top_frame, image=ctk_img, text="")
       img_label.place(relx=0.95, rely=0.15)
       text_label = ctk.CTkLabel(top_frame, text=f"Hello {self.user_name}", font=("Arial", 13), text_color='black')
       text_label.place(relx=0.88, rely=0.27)
       img_label.bind("<Button-1>", show_akun_page)  # Memasang event handler untuk menampilkan halaman akun

       # Menambahkan border bawah pada frame atas
       bottom_border = ctk.CTkFrame(top_frame, height=4, fg_color='#FECE8C', corner_radius=0)
       bottom_border.place(relx=0.0, rely=1.0, relwidth=1.0, anchor='sw')

       main_frame = ctk.CTkFrame(container_frame, fg_color='#E5E5E5', corner_radius=0)  # Membuat frame utama dengan modul customtkinter
       main_frame.grid(row=1, column=1, sticky="nsew")  # Meletakkan frame utama di grid tkinter

       main_frame.grid_rowconfigure(0, weight=1)  # Mengatur konfigurasi baris grid pada frame utama
       main_frame.grid_rowconfigure(1, weight=1)
       main_frame.grid_rowconfigure(2, weight=1)
       main_frame.grid_columnconfigure(0, weight=1)  # Mengatur konfigurasi kolom grid pada frame utama
       main_frame.grid_columnconfigure(1, weight=1)
       main_frame.grid_columnconfigure(2, weight=1)

       # Membuat frame untuk halaman akun dengan spesifikasi ukuran dan warna
       akun_frame = ctk.CTkFrame(main_frame, width=890, height=500, fg_color='white', corner_radius=10)
       akun_frame.place(relx=0.04, rely=0.05, relwidth=0.92, relheight=0.9)

       # Menampilkan gambar di atas halaman akun
       img_path = "img5.png"
       img = Image.open(img_path)
       img = img.resize((200, 200), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))
       img_label = ctk.CTkLabel(akun_frame, image=ctk_img, text="")
       img_label.place(relx=0.08, rely=0.1)

       # Label untuk judul "Pengaturan Akun"
       expense_label = ctk.CTkLabel(akun_frame, text="Pengaturan Akun", font=("Arial", 20, 'bold'))
       expense_label.place(relx=0.4, rely=0.08)

       # Label dan entry field untuk nama
       self.name_label = ctk.CTkLabel(akun_frame, text="Nama", font=("Poppins", 12))
       self.name_label.place(relx=0.4, rely=0.17)
       self.name_entry = ctk.CTkEntry(akun_frame, border_color='black')
       self.name_entry.place(relx=0.4, rely=0.22, relwidth=0.5)

       # Label dan entry field untuk email
       self.email_label = ctk.CTkLabel(akun_frame, text="Email", font=("Poppins", 12))
       self.email_label.place(relx=0.4, rely=0.32)
       self.email_entry = ctk.CTkEntry(akun_frame, border_color='black')
       self.email_entry.place(relx=0.4, rely=0.37, relwidth=0.5)

       # Label dan entry field untuk password
       self.password_label = ctk.CTkLabel(akun_frame, text="Password", font=("Poppins", 12))
       self.password_label.place(relx=0.4, rely=0.47)
       self.password_entry = ctk.CTkEntry(akun_frame, border_color='black')
       self.password_entry.place(relx=0.4, rely=0.52, relwidth=0.5)

       # Label dan entry field untuk nomor telepon
       self.telepon_label = ctk.CTkLabel(akun_frame, text="Telepon", font=("Poppins", 12))
       self.telepon_label.place(relx=0.4, rely=0.62)
       self.telepon_entry = ctk.CTkEntry(akun_frame, border_color='black')
       self.telepon_entry.place(relx=0.4, rely=0.67, relwidth=0.5)

       # Frame untuk tombol "Ubah Data Akun"
       ganti_data = ctk.CTkFrame(akun_frame, fg_color="black")
       ganti_data.place(relx=0.57, rely=0.77, relwidth=0.18, relheight=0.06)
       self.change_img_button = ctk.CTkButton(ganti_data, text="Ubah Data Akun", font=('Helvetica', 12, 'bold'),
                                              fg_color='#FECE8E', text_color='white', width=150, height=27,
                                              command=self.update_account_data)
       self.change_img_button.pack(expand=True)

       # Frame untuk tombol "Log Out"
       logout = ctk.CTkFrame(akun_frame, fg_color="black")
       logout.place(relx=0.57, rely=0.85, relwidth=0.18, relheight=0.06)
       self.change_img_button = ctk.CTkButton(logout, text="Log Out", font=('Helvetica', 12, 'bold'),
                                              fg_color='red', text_color='white', width=150, height=26,
                                              command=self.logout)
       self.change_img_button.pack(expand=True)

       # Fungsi untuk menampilkan halaman dashboard
       def show_dashboard(self):
           from dashboard_tab import Dashboard
           dashboard = Dashboard(self.root, self.current_user_id, self.user_name)
           dashboard.show_dashboard()

       # Fungsi untuk menampilkan halaman pencatatan
       def show_Pencatatan(self):
           from pencatatan_tab import Pencatatan
           pencatatan = Pencatatan(self.root, self.current_user_id, self.user_name)
           pencatatan.show_Pencatatan()

       # Fungsi untuk menampilkan halaman informasi
       def show_Info(self):
           from info_tab import Info
           info = Info(self.root, self.current_user_id, self.user_name)
           info.show_Info()

       # Fungsi untuk mengupdate data akun di database
       def update_account_data(self):
           try:
               with cn.cursor() as cursor:
                   name = self.name_entry.get()
                   email = self.email_entry.get()
                   password = self.password_entry.get()
                   telepon = self.telepon_entry.get()
                   cursor.execute(
                       "UPDATE data SET nama = %s, email = %s, password = %s, telepon = %s WHERE id = %s",
                       (name, email, password, telepon, self.current_user_id)
                   )
                   cn.commit()
               messagebox.showinfo("Sukses", "Pengaturan akun berhasil disimpan")
           except Exception as e:
               messagebox.showerror("Error", f"Gagal menyimpan pengaturan akun: {e}")

       # Fungsi untuk melakukan proses logout
       def logout(self):
           from login_tab import LoginTab
           login = LoginTab(self.root)
           login.login()
