import customtkinter as ctk  # Mengimpor pustaka customtkinter untuk pembuatan antarmuka pengguna.
from PIL import Image  # Mengimpor PIL untuk manipulasi gambar.
from database import cn  # Mengimpor koneksi database dari modul database.
from tkinter import Scrollbar, messagebox  # Mengimpor Scrollbar dan messagebox dari tkinter.

class Pencatatan:
   def __init__(self, root, user_id, user_name):
       self.root = root  # Menyimpan referensi ke root window.
       self.user_id = user_id  # Menyimpan ID pengguna.
       self.user_name = user_name  # Menyimpan nama pengguna.
       self.root.geometry("1000x600")  # Mengatur ukuran jendela root.

   def pemasukan(self, nama, nominal, bulan):
       cursor = cn.cursor()  # Membuat kursor untuk operasi database.
       cursor.execute("INSERT INTO pemasukan (user_id, nama, nominal, bulan) VALUES (%s, %s, %s, %s)",
                      (self.user_id, nama, nominal, bulan))  # Menyisipkan data pemasukan ke dalam tabel database.
       cn.commit()  # Menyimpan perubahan ke database.
       cursor.close()  # Menutup kursor.
       self.update_history()  # Memperbarui sejarah transaksi.

   def pengeluaran(self, nama, nominal, bulan):
       cursor = cn.cursor()  # Membuat kursor untuk operasi database.
       cursor.execute("INSERT INTO pengeluaran (user_id, nama, nominal, bulan) VALUES (%s, %s, %s, %s)",
                      (self.user_id, nama, nominal, bulan))  # Menyisipkan data pengeluaran ke dalam tabel database.
       cn.commit()  # Menyimpan perubahan ke database.
       cursor.close()  # Menutup kursor.
       self.update_history()  # Memperbarui sejarah transaksi.

   def fetch_transactions(self, jenis, bulan):
       cursor = cn.cursor()  # Membuat kursor untuk operasi database.

       user_condition = f"user_id = {self.user_id}"  # Membuat kondisi untuk menyaring transaksi berdasarkan user_id.

       if jenis == "Pemasukan":
           query = f"SELECT 'pemasukan' as jenis, nama, nominal, bulan FROM pemasukan WHERE {user_condition}"
       elif jenis == "Pengeluaran":
           query = f"SELECT 'pengeluaran' as jenis, nama, nominal, bulan FROM pengeluaran WHERE {user_condition}"
       else:
           query = f"(SELECT 'pemasukan' as jenis, nama, nominal, bulan FROM pemasukan WHERE {user_condition}) UNION ALL (SELECT 'pengeluaran' as jenis, nama, nominal, bulan FROM pengeluaran WHERE {user_condition})"
           # Menyusun query untuk pemasukan, pengeluaran, atau gabungan keduanya.

       if bulan != "Semua" and bulan != "Pilih Bulan":
           if "UNION" in query:
               query = f"SELECT * FROM ({query}) AS combined WHERE bulan = '{bulan}' ORDER BY FIELD(bulan, 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember')"
           else:
               query += f" AND bulan = '{bulan}' ORDER BY FIELD(bulan, 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember')"
           # Menambahkan kondisi untuk menyaring berdasarkan bulan dan mengurutkan berdasarkan urutan bulan.
       else:
           if "UNION" in query:
               query = f"SELECT * FROM ({query}) AS combined ORDER BY FIELD(bulan, 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember')"
           else:
               query += f" ORDER BY FIELD(bulan, 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember')"
           # Mengurutkan berdasarkan bulan jika semua bulan dipilih.

       cursor.execute(query)  # Menjalankan query di database.
       transactions = cursor.fetchall()  # Mengambil semua hasil query.

       cursor.close()  # Menutup kursor.
       return transactions  # Mengembalikan hasil transaksi.

   def show_Pencatatan(self):
       for widget in self.root.winfo_children():
           widget.destroy()  # Menghancurkan semua widget dalam root window.
       self.root.grid_rowconfigure(0, weight=1)
       self.root.grid_columnconfigure(0, weight=1)

       def show_dashboard_page(event=None):
           self.show_dashboard()  # Menampilkan halaman dashboard.

       def show_pencatatan_page(event=None):
           self.show_Pencatatan()  # Menampilkan halaman pencatatan.

       def show_info_page(event=None):
           self.show_Info()  # Menampilkan halaman info.

       def show_akun_page(event=None):
           self.show_Akun()  # Menampilkan halaman akun.

       container_frame = ctk.CTkFrame(self.root, fg_color='white', corner_radius=0)
       container_frame.grid(row=0, column=0, sticky="nsew")
       container_frame.grid_rowconfigure(1, weight=1)
       container_frame.grid_columnconfigure(1, weight=1)
       # Membuat container frame dan mengatur grid.

       left_frame = ctk.CTkFrame(container_frame, width=60, height=600, fg_color='white', corner_radius=0)
       left_frame.grid(row=1, column=0, sticky="nsew")
       # Membuat frame kiri dan mengatur posisinya.

       top_frame = ctk.CTkFrame(container_frame, height=50, fg_color='white', corner_radius=0)
       top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
       # Membuat frame atas dan mengatur posisinya.

       img_path = "img1.PNG"
       img = Image.open(img_path)
       img = img.resize((50, 50), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(48, 48))
       # Membuka dan mengubah ukuran gambar untuk penggunaan di widget.

       img_label = ctk.CTkLabel(top_frame, image=ctk_img, text="")
       img_label.place(relx=0.005, rely=0.12)
       # Membuat label gambar dan menempatkannya di frame atas.

       text_label = ctk.CTkLabel(top_frame, text="MY FINANCE", font=("Arial", 16, 'bold'), text_color='orange')
       text_label.place(relx=0.06, rely=0.27)
       # Membuat label teks dan menempatkannya di frame atas.

       img_path = "img3.PNG"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(38, 38))
       # Membuka dan mengubah ukuran gambar lain untuk penggunaan di widget.

       img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
       img_label.place(relx=0.18, rely=0.35)
       text_label = ctk.CTkLabel(left_frame, text="Dashboard", font=("Arial", 8), text_color='gray')
       text_label.place(relx=0.15, rely=0.41)
       img_label.bind("<Button-1>", show_dashboard_page)
       # Membuat label gambar dan teks untuk dashboard dan menempatkannya di frame kiri.

       img_path = "img4.PNG"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(33, 33))
       # Membuka dan mengubah ukuran gambar lain untuk penggunaan di widget.

       img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
       img_label.place(relx=0.30, rely=0.47)
       text_label = ctk.CTkLabel(left_frame, text="Pencatatan", font=("Arial", 8), text_color='gray')
       text_label.place(relx=0.15, rely=0.53)
       img_label.bind("<Button-1>", show_pencatatan_page)
       # Membuat label gambar dan teks untuk pencatatan dan menempatkannya di frame kiri.

       img_path = "img6.png"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
       # Membuka dan mengubah ukuran gambar lain untuk penggunaan di widget.

       img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
       img_label.place(relx=0.14, rely=0.88)
       text_label = ctk.CTkLabel(left_frame, text="Info", font=("Arial", 8), text_color='gray')
       text_label.place(relx=0.38, rely=0.94)
       img_label.bind("<Button-1>", show_info_page)
       # Membuat label gambar dan teks untuk info dan menempatkannya di frame kiri.

       img_path = "img5.png"
       img = Image.open(img_path)
       img = img.resize((100, 100), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(35, 35))
       # Membuka dan mengubah ukuran gambar lain untuk penggunaan di widget.

       img_label = ctk.CTkLabel(top_frame, image=ctk_img, text="")
       img_label.place(relx=0.95, rely=0.15)
       text_label = ctk.CTkLabel(top_frame, text=f"Hello {self.user_name}", font=("Arial", 13), text_color='black')
       text_label.place(relx=0.88, rely=0.27)
       img_label.bind("<Button-1>", show_akun_page)
       # Membuat label gambar dan teks untuk akun dan menempatkannya di frame atas.

       bottom_border = ctk.CTkFrame(top_frame, height=4, fg_color='#FECE8C', corner_radius=0)
       bottom_border.place(relx=0.0, rely=1.0, relwidth=1.0, anchor='sw')
       # Membuat border bawah di frame atas.

       main_frame = ctk.CTkFrame(container_frame, fg_color='#E5E5E5', corner_radius=0)
       main_frame.grid(row=1, column=1, sticky="nsew")
       # Membuat main frame dan menempatkannya di container frame.

       main_frame.grid_rowconfigure(0, weight=1)
       main_frame.grid_rowconfigure(1, weight=1)
       main_frame.grid_rowconfigure(2, weight=1)
       main_frame.grid_columnconfigure(0, weight=1)
       main_frame.grid_columnconfigure(1, weight=1)
       main_frame.grid_columnconfigure(2, weight=1)
       # Mengatur konfigurasi grid untuk main frame.

# Frame untuk Pemasukan
   income_frame = ctk.CTkFrame(main_frame, fg_color='white', corner_radius=10)
   income_frame.place(relx=0.04, rely=0.02, relwidth=0.5, relheight=0.46)

   # Label untuk judul pemasukan
   income_label = ctk.CTkLabel(income_frame, text="Silahkan Input Pemasukan Anda", font=("Arial", 16, 'bold'))
   income_label.place(relx=0.05, rely=0.05, relwidth=0.9)

   # Label untuk Nama Pemasukan
   self.income_name_label = ctk.CTkLabel(income_frame, text="Nama Pemasukan", font=("Poppins", 12))
   self.income_name_label.place(relx=0.05, rely=0.15)

   # Entry untuk Nama Pemasukan
   self.income_name_entry = ctk.CTkEntry(income_frame, border_color='black')
   self.income_name_entry.place(relx=0.05, rely=0.24, relwidth=0.9)

   # Label untuk Nominal Pemasukan
   self.income_amount_label = ctk.CTkLabel(income_frame, text="Nominal Pemasukan", font=("Poppins", 12))
   self.income_amount_label.place(relx=0.05, rely=0.35)

   # Entry untuk Nominal Pemasukan
   self.income_amount_entry = ctk.CTkEntry(income_frame, border_color='black')
   self.income_amount_entry.place(relx=0.05, rely=0.44, relwidth=0.9)

   # Label untuk Pilih Bulan
   self.month_label = ctk.CTkLabel(income_frame, text="Pilih Bulan", font=("Poppins", 12))
   self.month_label.place(relx=0.05, rely=0.55)

   # Dropdown menu untuk memilih bulan
   self.month_va = ctk.StringVar(value="Januari")
   self.month_menu = ctk.CTkOptionMenu(income_frame, variable=self.month_va,
                                       values=["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
                                               "Agustus", "September", "Oktober", "November", "Desember"],
                                       fg_color='#FECE8C', text_color='black', button_color='orange',
                                       dropdown_fg_color='white', dropdown_hover_color='#FECE8C',
                                       button_hover_color='#E5E5E5', anchor="w")
   self.month_menu.place(relx=0.05, rely=0.64, relwidth=0.9)

   # Frame untuk tombol Tambah Pemasukan
   add_income_button = ctk.CTkFrame(income_frame, fg_color="black")
   add_income_button.place(relx=0.5, rely=0.87, relwidth=0.223, relheight=0.115, anchor='center')

   # Tombol Tambah Pemasukan
   self.register_button = ctk.CTkButton(add_income_button, text="Tambah", font=('Helvetica', 12, 'bold'),
                                        fg_color='#FECE8E', text_color='white', width=100, height=26,
                                        command=self.handle_add_income)
   self.register_button.pack(expand=True)

   # Frame untuk Pengeluaran
   expense_frame = ctk.CTkFrame(main_frame, fg_color='white', corner_radius=10)
   expense_frame.place(relx=0.04, rely=0.5, relwidth=0.5, relheight=0.48)

   # Label untuk judul pengeluaran
   expense_label = ctk.CTkLabel(expense_frame, text="Silahkan Input Pengeluaran Anda", font=("Arial", 16, 'bold'))
   expense_label.place(relx=0.05, rely=0.05, relwidth=0.9)

   # Label untuk Nama Pengeluaran
   self.expense_name_label = ctk.CTkLabel(expense_frame, text="Nama Pengeluaran", font=("Poppins", 12))
   self.expense_name_label.place(relx=0.05, rely=0.15)

   # Entry untuk Nama Pengeluaran
   self.expense_name_entry1 = ctk.CTkEntry(expense_frame, border_color='black')
   self.expense_name_entry1.place(relx=0.05, rely=0.24, relwidth=0.9)

   # Label untuk Nominal Pengeluaran
   self.expense_amount_label = ctk.CTkLabel(expense_frame, text="Nominal Pengeluaran", font=("Poppins", 12))
   self.expense_amount_label.place(relx=0.05, rely=0.35)

   # Entry untuk Nominal Pengeluaran
   self.expense_amount_entry1 = ctk.CTkEntry(expense_frame, border_color='black')
   self.expense_amount_entry1.place(relx=0.05, rely=0.44, relwidth=0.9)

   # Label untuk Pilih Bulan
   self.month_label = ctk.CTkLabel(expense_frame, text="Pilih Bulan", font=("Poppins", 12))
   self.month_label.place(relx=0.05, rely=0.55)

   # Dropdown menu untuk memilih bulan
   self.month_var = ctk.StringVar(value="Januari")
   self.month_menu = ctk.CTkOptionMenu(expense_frame, variable=self.month_var,
                                       values=["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
                                               "Agustus", "September", "Oktober", "November", "Desember"],
                                       fg_color='#FECE8C', text_color='black', button_color='orange',
                                       dropdown_fg_color='white', dropdown_hover_color='#FECE8C',
                                       button_hover_color='#E5E5E5', anchor="w")
   self.month_menu.place(relx=0.05, rely=0.64, relwidth=0.9)

   # Frame untuk tombol Tambah Pengeluaran
   add_expense_button = ctk.CTkFrame(expense_frame, fg_color="black")
   add_expense_button.place(relx=0.5, rely=0.87, relwidth=0.223, relheight=0.115, anchor='center')

   # Tombol Tambah Pengeluaran
   self.register_button = ctk.CTkButton(add_expense_button, text="Tambah", font=('Helvetica', 12, 'bold'),
                                        fg_color='#FECE8E', text_color='white', width=100, height=26,
                                        command=self.handle_add_expense)
   self.register_button.pack(expand=True)

   # Frame untuk Riwayat
   history_frame = ctk.CTkFrame(main_frame, fg_color='white', corner_radius=10)
   history_frame.place(relx=0.58, rely=0.02, relwidth=0.38, relheight=0.96)

   # Label untuk judul riwayat
   history_label = ctk.CTkLabel(history_frame, text="Riwayat", font=("Arial", 16, 'bold'))
   history_label.place(relx=0.5, rely=0.05, anchor='center')

   # Variable untuk tipe transaksi
   self.transaction_type_var = ctk.StringVar()
   self.transaction_type_var.set("Pilih Riwayat")

   # Dropdown menu untuk memilih tipe transaksi
   transaction_type_options = ["Semua", "Pemasukan", "Pengeluaran"]
   self.transaction_type_menu = ctk.CTkOptionMenu(history_frame, variable=self.transaction_type_var,
                                                  values=transaction_type_options,
                                                  fg_color='#FECE8C', text_color='black', button_color='orange',
                                                  dropdown_fg_color='white', dropdown_hover_color='#FECE8C',
                                                  button_hover_color='#E5E5E5')
   self.transaction_type_menu.place(relx=0.05, rely=0.1, relwidth=0.9)

   # Variable untuk bulan
   self.month_var = ctk.StringVar()
   self.month_var.set("Pilih Bulan")

   # Dropdown menu untuk memilih bulan
   month_options = ["Semua", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
                    "September", "Oktober", "November", "Desember"]
   self.month_menu = ctk.CTkOptionMenu(history_frame, variable=self.month_var, values=month_options,
                                       fg_color='#FECE8C', text_color='black', button_color='orange',
                                       dropdown_fg_color='white', dropdown_hover_color='#FECE8C',
                                       button_hover_color='#E5E5E5')
   self.month_menu.place(relx=0.05, rely=0.17, relwidth=0.9)

   # Frame untuk menampung riwayat transaksi
   self.history_container = ctk.CTkFrame(history_frame, fg_color='white', corner_radius=10)
   self.history_container.place(relx=0.5, rely=0.3, relwidth=0.9, relheight=0.7, anchor='n')

   # Canvas untuk riwayat transaksi
   self.history_canvas = ctk.CTkCanvas(self.history_container, bg='white', highlightthickness=0)
   self.history_canvas.place(relx=0, rely=0, relwidth=0.95, relheight=1)

   # Scrollbar untuk riwayat transaksi
   self.scrollbar = Scrollbar(self.history_container, orient='vertical', command=self.history_canvas.yview)
   self.scrollbar.place(relx=0.95, rely=0, relheight=1)

   # Mengkonfigurasi canvas dengan scrollbar
   self.history_canvas.configure(yscrollcommand=self.scrollbar.set)
   self.history_frame_inner = ctk.CTkFrame(self.history_canvas, fg_color='white')

   # Menempatkan frame inner ke dalam canvas
   self.history_canvas.create_window((0, 0), window=self.history_frame_inner, anchor='nw')

   # Mengupdate canvas saat frame inner berubah ukuran
   self.history_frame_inner.bind("<Configure>",
                                 lambda e: self.history_canvas.configure(
                                     scrollregion=self.history_canvas.bbox("all")))

   # Menambahkan trace untuk mengupdate riwayat
   self.transaction_type_var.trace("w", lambda *args: self.update_history())
   self.month_var.trace("w", lambda *args: self.update_history())

   # Memperbarui riwayat saat inisialisasi
   self.update_history()

# Fungsi untuk menangani penambahan pemasukan
def handle_add_income(self):
   nama = self.income_name_entry.get()
   nominal = self.income_amount_entry.get()
   bulan = self.month_va.get()

   # Validasi input
   if not nama or not nominal or bulan == "Pilih Bulan":
       messagebox.showerror("Error", "Semua input harus diisi.")
       return

   try:
       nominal = int(nominal)
       if nominal < 0:
           raise ValueError("Nominal harus bernilai positif")
   except ValueError as e:
       messagebox.showerror("Error", str(e))
       return

   # Memanggil fungsi pemasukan dan memperbarui riwayat
   self.pemasukan(nama, nominal, bulan)
   self.income_name_entry.delete(0, 'end')
   self.income_amount_entry.delete(0, 'end')
   self.month_va.set("Pilih Bulan")
   self.update_history()

# Fungsi untuk menangani penambahan pengeluaran
def handle_add_expense(self):
   nama = self.expense_name_entry1.get()
   nominal = self.expense_amount_entry1.get()
   bulan = self.month_var.get()

   # Validasi input
   if not nama atau tidak nominal atau bulan == "Pilih Bulan":
       messagebox.showerror("Error", "Semua input harus diisi.")
       return

   try:
       nominal = int(nominal)
       if nominal < 0:
           raise ValueError("Nominal harus bernilai positif")
   except ValueError as e:
       messagebox.showerror("Error", str(e))
       return

   # Memanggil fungsi pengeluaran dan memperbarui riwayat
   self.pengeluaran(nama, nominal, bulan)
   self.expense_name_entry1.delete(0, 'end')
   self.expense_amount_entry1.delete(0, 'end')
   self.month_var.set("Pilih Bulan")
   self.update_history()

# Fungsi untuk memperbarui riwayat transaksi
def update_history(self):
   # Menghapus widget lama di frame inner
   for widget in self.history_frame_inner.winfo_children():
       widget.destroy()

   # Mendapatkan tipe transaksi dan bulan yang dipilih
   jenis = self.transaction_type_var.get()
   bulan = self.month_var.get()
   transactions = self.fetch_transactions(jenis, bulan)

   # Menambahkan transaksi baru ke frame inner
   for transaction in transactions:
       transaction_label = ctk.CTkLabel(
           self.history_frame_inner,
           text=f"{transaction[0]}: {transaction[1]} - {transaction[2]} ({transaction[3]})",
           font=("Arial", 12),
           wraplength=300,
           justify="left"
       )
       transaction_label.pack(anchor='w', padx=10, pady=2)

# Fungsi untuk menampilkan dashboard
def show_dashboard(self):
   from dashboard_tab import Dashboard
   dashboard = Dashboard(self.root, user_id=self.user_id, user_name= self.user_name)
   dashboard.show_dashboard()

# Fungsi untuk menampilkan Info
def show_Info(self):
   from info_tab import Info
   info = Info(self.root, user_id=self.user_id, user_name= self.user_name)
   info.show_Info()

# Fungsi untuk menampilkan Akun
def show_Akun(self):
   from akun_tab import Akun
   akun = Akun(self.root, user_id=self.user_id, user_name= self.user_name)
   akun.show_Akun()
