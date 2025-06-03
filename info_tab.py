import customtkinter as ctk  # Mengimport customtkinter sebagai ctk
from PIL import Image  # Mengimport Image dari PIL (Pillow)

class Info:
   def __init__(self, root, user_id, user_name):
       self.root = root  # Menyimpan root window
       self.user_id = user_id  # Menyimpan user_id
       self.user_name = user_name  # Menyimpan user_name
       self.root.geometry("1000x600")  # Mengatur ukuran jendela aplikasi

   def show_Info(self):
       for widget in self.root.winfo_children():
           widget.destroy()  # Menghapus semua widget di dalam root window
       self.root.grid_rowconfigure(0, weight=1)  # Mengatur konfigurasi baris untuk root window
       self.root.grid_columnconfigure(0, weight=1)  # Mengatur konfigurasi kolom untuk root window

       def show_dashboard_page(event=None):
           self.show_dashboard()  # Fungsi untuk menampilkan halaman dashboard

       def show_pencatatan_page(event=None):
           self.show_Pencatatan()  # Fungsi untuk menampilkan halaman pencatatan

       def show_info_page(event=None):
           self.show_Info()  # Fungsi untuk menampilkan halaman info (self)

       def show_akun_page(event=None):
           self.show_Akun()  # Fungsi untuk menampilkan halaman akun

       container_frame = ctk.CTkFrame(self.root, fg_color='white', corner_radius=0)  # Membuat frame container
       container_frame.grid(row=0, column=0, sticky="nsew")  # Meletakkan frame container di root window
       container_frame.grid_rowconfigure(1, weight=1)  # Mengatur konfigurasi baris untuk frame container
       container_frame.grid_columnconfigure(1, weight=1)  # Mengatur konfigurasi kolom untuk frame container

       left_frame = ctk.CTkFrame(container_frame, width=60, height=600, fg_color='white', corner_radius=0)  # Membuat frame kiri
       left_frame.grid(row=1, column=0, sticky="nsew")  # Meletakkan frame kiri di dalam frame container

       top_frame = ctk.CTkFrame(container_frame, height=50, fg_color='white', corner_radius=0)  # Membuat frame atas
       top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")  # Meletakkan frame atas di dalam frame container

       # Menyiapkan dan menampilkan gambar di label di bagian atas aplikasi
       img_path = "img1.PNG"
       img = Image.open(img_path)
       img = img.resize((50, 50), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(48, 48))
       img_label = ctk.CTkLabel(top_frame, image=ctk_img, text="")
       img_label.place(relx=0.005, rely=0.12)

       # Menampilkan teks "MY FINANCE" di bagian atas aplikasi
       text_label = ctk.CTkLabel(top_frame, text="MY FINANCE", font=("Arial", 16, 'bold'), text_color='orange')
       text_label.place(relx=0.06, rely=0.27)

       # Menyiapkan dan menampilkan menu navigasi kiri
       img_path = "img3.PNG"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(38, 38))
       img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
       img_label.place(relx=0.18, rely=0.35)
       text_label = ctk.CTkLabel(left_frame, text="Dashboard", font=("Arial", 8), text_color='gray')
       text_label.place(relx=0.15, rely=0.41)
       img_label.bind("<Button-1>", show_dashboard_page)

       img_path = "img4.PNG"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(33, 33))
       img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
       img_label.place(relx=0.30, rely=0.47)
       text_label = ctk.CTkLabel(left_frame, text="Pencatatan", font=("Arial", 8), text_color='gray')
       text_label.place(relx=0.15, rely=0.53)
       img_label.bind("<Button-1>", show_pencatatan_page)

       img_path = "img6.png"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
       img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
       img_label.place(relx=0.14, rely=0.88)
       text_label = ctk.CTkLabel(left_frame, text="Info", font=("Arial", 8), text_color='gray')
       text_label.place(relx=0.38, rely=0.94)
       img_label.bind("<Button-1>", show_info_page)

       # Menyiapkan dan menampilkan gambar di bagian kanan atas aplikasi
       img_path = "img5.png"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(35, 35))
       img_label = ctk.CTkLabel(top_frame, image=ctk_img, text="")
       img_label.place(relx=0.95, rely=0.15)
       text_label = ctk.CTkLabel(top_frame, text=f"Hello {self.user_name}", font=("Arial", 13), text_color='black')
       text_label.place(relx=0.88, rely=0.27)
       img_label.bind("<Button-1>", show_akun_page)

       # Menyiapkan garis bawah di bagian bawah frame atas
       bottom_border = ctk.CTkFrame(top_frame, height=4, fg_color='#FECE8C', corner_radius=0)
       bottom_border.place(relx=0.0, rely=1.0, relwidth=1.0, anchor='sw')

       # Menyiapkan frame utama di sebelah kanan aplikasi
       main_frame = ctk.CTkFrame(container_frame, fg_color='#E5E5E5', corner_radius=0)
       main_frame.grid(row=1, column=1, sticky="nsew")

       main_frame.grid_rowconfigure(0, weight=1)  # Mengatur konfigurasi baris untuk frame utama
       main_frame.grid_rowconfigure(1, weight=1)  # Mengatur konfigurasi baris untuk frame utama
       main_frame.grid_rowconfigure(2, weight=1)  # Mengatur konfigurasi baris untuk frame utama
       main_frame.grid_columnconfigure(0, weight=1)  # Mengatur konfigurasi kolom untuk frame utama
       main_frame.grid_columnconfigure(1, weight=1)  # Mengatur konfigurasi kolom untuk frame utama
       main_frame.grid_columnconfigure(2, weight=1)  # Mengatur konfigurasi kolom untuk frame utama

       # Menyiapkan frame informasi di dalam frame utama
       info_frame = ctk.CTkFrame(main_frame, width=890, height=500, fg_color='white', corner_radius=10)
       info_frame.place(relx=0.04, rely=0.05, relwidth=0.92, relheight=0.9)
       text_label = ctk.CTkLabel(info_frame,
                                 text="Tentang Aplikasi",
                                 font=("Arial", 25, 'bold'),
                                 text_color='black')
       text_label.place(relx=0.5, rely=0.05, anchor='n')

       # Menyiapkan dan menampilkan gambar di dalam frame informasi
       img_path = "img2.PNG"
       img = Image.open(img_path)
       img = img.resize((500, 500), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(30, 30))
       img_label = ctk.CTkLabel(info_frame, image=ctk_img, text="")
       img_label.place(relx=0.03, rely=0.9, anchor="w")
       img_label.bind("<Button-1>", lambda e: self.show_dashboard())

       # Menyiapkan dan menampilkan paragraf teks di dalam frame informasi
      
       paragraph = '''Selamat datang di My Finance, aplikasi pencatatan keuangan yang dirancang untuk membantu Anda mengelola
               keuangan dengan lebih mudah dan efektif. Dengan fitur pencatatan pemasukan dan pengeluaran yang intuitif,
               My Finance memungkinkan Anda untuk memonitor arus kas harian, bulanan, hingga tahunan. Selain itu, aplikasi ini
               dilengkapi dengan grafik keuangan yang interaktif, memudahkan Anda untuk menganalisis tren keuangan pribadi dan
               membuat keputusan finansial yang lebih bijak. Kami berkomitmen untuk memberikan Anda alat yang sederhana
               namun kuat, agar pengelolaan keuangan menjadi lebih teratur dan transparan. Mari mulai perjalanan keuangan Anda
               bersama My Finance dan raih kestabilan finansial yang Anda impikan!'''
      
       lines = paragraph.split('\n')
      
       for i, line in enumerate(lines):
           text_label = ctk.CTkLabel(info_frame,
                                     text=line.strip(),
                                     font=("Arial", 15, 'bold'),
                                     text_color='black')
           text_label.place(relx=0.04, rely=0.15 + (i * 0.05), relwidth=0.92, anchor='nw')
       # Komentar:
       # - Memecah paragraf menjadi baris dan membuat label untuk setiap baris dalam komponen GUI.
       # - Setiap label ditempatkan pada posisi tertentu di dalam frame.
      
       def show_dashboard(self):
           from dashboard_tab import Dashboard
           dashboard = Dashboard(self.root, user_id=self.user_id, user_name=self.user_name)
           dashboard.show_dashboard()
       # Komentar:
       # - Mengimpor dan menampilkan dashboard menggunakan sebuah kelas dari 'dashboard_tab'.
       # - Metode ini tampaknya menginisiasi tampilan dashboard pengguna.
      
       def show_Pencatatan(self):
           from pencatatan_tab import Pencatatan
           pencatatan = Pencatatan(self.root, user_id=self.user_id, user_name=self.user_name)
           pencatatan.show_Pencatatan()
       # Komentar:
       # - Mengimpor dan menampilkan tab 'Pencatatan' menggunakan sebuah kelas dari 'pencatatan_tab'.
       # - Metode ini bertanggung jawab untuk menampilkan tab yang terkait dengan catatan keuangan.
      
       def show_Akun(self):
           from akun_tab import Akun
           akun = Akun(self.root, user_id=self.user_id, user_name=self.user_name)
           akun.show_Akun()
       # Komentar:
       # - Mengimpor dan menampilkan tab 'Akun' menggunakan sebuah kelas dari 'akun_tab'.
       # - Metode ini bertugas menampilkan tab yang berkaitan dengan akun dalam aplikasi.
