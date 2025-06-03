import customtkinter as ctk  # Import library customtkinter untuk membuat GUI
from PIL import Image  # Import library PIL untuk menangani gambar
from matplotlib import pyplot as plt  # Import library matplotlib untuk membuat grafik
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import backend TkAgg dari matplotlib untuk integrasi dengan tkinter
import matplotlib.ticker as ticker  # Import ticker dari matplotlib untuk format axis
import numpy as np  # Import library numpy untuk komputasi numerik
from database import cn  # Import koneksi database

class Dashboard:
   def __init__(self, root, user_id, user_name):
       self.root = root  # Set root GUI
       self.user_id = user_id  # Set user ID
       self.user_name = user_name  # Set user name
       self.after_id = None  # Initialize variabel untuk menyimpan ID after
       self.root.geometry("1000x600")  # Set ukuran window
       self.frame_ids = {}  # Dictionary untuk menyimpan frame ID

   def get_financial_data(self, month=None):
       cursor = cn.cursor()  # Membuat cursor untuk eksekusi query
       user_condition = f"user_id = {self.user_id}"  # Kondisi query berdasarkan user_id

       query_pemasukan = f"SELECT SUM(nominal) FROM pemasukan WHERE {user_condition}"  # Query untuk mendapatkan total pemasukan
       query_pengeluaran = f"SELECT SUM(nominal) FROM pengeluaran WHERE {user_condition}"  # Query untuk mendapatkan total pengeluaran

       if month and month != "Semua" and month != "Pilih Bulan":
           query_pemasukan += f" AND bulan = '{month}'"  # Tambahkan filter bulan ke query pemasukan
           query_pengeluaran += f" AND bulan = '{month}'"  # Tambahkan filter bulan ke query pengeluaran

       cursor.execute(query_pemasukan)  # Eksekusi query pemasukan
       total_pemasukan = cursor.fetchone()[0] or 0  # Ambil hasil query pemasukan, default 0 jika None

       cursor.execute(query_pengeluaran)  # Eksekusi query pengeluaran
       total_pengeluaran = cursor.fetchone()[0] or 0  # Ambil hasil query pengeluaran, default 0 jika None

       sisa_uang = total_pemasukan - total_pengeluaran  # Hitung sisa uang

       cursor.close()  # Tutup cursor
       return total_pemasukan, total_pengeluaran, sisa_uang  # Kembalikan total pemasukan, pengeluaran, dan sisa uang

   def show_bar_chart(self, frame, data_type):
       frame_id = f"chart_{len(self.frame_ids) + 1}"  # Buat ID unik untuk frame grafik
       self.frame_ids[frame] = frame_id  # Simpan ID frame

       pemasukan_months, pemasukan_data = self.fetch_pemasukan_per_month()  # Ambil data pemasukan per bulan
       pengeluaran_months, pengeluaran_data = self.fetch_pengeluaran_per_month()  # Ambil data pengeluaran per bulan

       if data_type == 'pemasukan':
           months = pemasukan_months  # Set bulan untuk pemasukan
           data = pemasukan_data  # Set data untuk pemasukan
           other_data = pengeluaran_data  # Set data pengeluaran untuk referensi
           color = '#97D3CB'  # Warna grafik pemasukan
           title = 'Grafik Pemasukan'  # Judul grafik pemasukan

           if data == 0 and other_data == 0:  # Jika tidak ada data, kosongkan frame
               for widget in frame.winfo_children():
                   widget.destroy()
               return

       elif data_type == 'pengeluaran':
           months = pengeluaran_months  # Set bulan untuk pengeluaran
           data = pengeluaran_data  # Set data untuk pengeluaran
           other_data = pemasukan_data  # Set data pemasukan untuk referensi
           color = '#FECE8C'  # Warna grafik pengeluaran
           title = 'Grafik Pengeluaran'  # Judul grafik pengeluaran

           if data == 0 and other_data == 0:  # Jika tidak ada data, kosongkan frame
               for widget in frame.winfo_children():
                   widget.destroy()
               return

       else:
           raise ValueError("Data type must be 'pemasukan' atau 'pengeluaran'.")  # Lempar error jika tipe data tidak valid

       short_months = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"]  # Daftar singkatan bulan

       fig, ax = plt.subplots()  # Buat figure dan axis baru

       bars = ax.bar(short_months, data, color=color)  # Buat bar chart

       ax.spines['top'].set_visible(False)  # Sembunyikan sumbu atas
       ax.spines['right'].set_visible(False)  # Sembunyikan sumbu kanan
       ax.spines['left'].set_visible(False)  # Sembunyikan sumbu kiri

       # Mengatur rentang y-axis secara dinamis
       max_data = max(data)  # Dapatkan nilai maksimum data
       max_other_data = max(other_data)  # Dapatkan nilai maksimum data lain

       if max_data == 0 and max_other_data > 0:
           max_data = max_other_data  # Jika data utama nol tetapi data lain ada, gunakan nilai data lain
       elif max_data == 0 and max_other_data == 0:
           max_data = 1  # Jika keduanya nol, set max_data ke 1

       if max_data > 0:
           y_ticks = np.linspace(0, max_data, num=6)  # Buat ticks y secara linier
           y_tick_labels = [f'{int(tick):,}' for tick in y_ticks]  # Buat label ticks y

           for tick in y_ticks:
               ax.axhline(tick, color='gray', linewidth=1, linestyle='--', alpha=0.5)  # Garis horizontal untuk setiap tick

           ax.axhline(0, color='gray', linewidth=1)  # Garis horizontal pada y=0
           ax.set_ylim(top=max_data * 1.1)  # Set limit atas y-axis
           ax.set_xlim(left=-0.5, right=11.5)  # Set limit x-axis
           ax.set_yticks(y_ticks)  # Set ticks y-axis
           ax.set_yticklabels(y_tick_labels)  # Set label ticks y-axis
           ax.set_yticklabels([])  # Kosongkan label y-axis untuk tampilan akhir

       ax.text(-0.20, 0.5, title, transform=ax.transAxes,
               fontsize=10, va='center', ha='center', rotation=90)  # Tambahkan judul di sisi grafik

       for widget in frame.winfo_children():  # Hapus semua widget dalam frame
           widget.destroy()

       canvas = FigureCanvasTkAgg(fig, master=frame)  # Buat canvas dari figure
       canvas.draw()  # Gambar canvas
       canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=1)  # Tempatkan canvas dalam frame

       fig.subplots_adjust(top=0.9, bottom=0.15, left=0.19, right=0.9)  # Atur margin figure
       canvas.draw()  # Gambar ulang canvas

       ax.yaxis.set_major_formatter(
           ticker.StrMethodFormatter('{x:,.0f}'))  # Format axis y

   def fetch_pemasukan_per_month(self):
       cursor = cn.cursor()  # Buat cursor untuk eksekusi query
       query = f"SELECT bulan, SUM(nominal) FROM pemasukan WHERE user_id = {self.user_id} GROUP BY bulan ORDER BY FIELD(bulan, 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember')"  # Query untuk pemasukan per bulan
       cursor.execute(query)  # Eksekusi query
       data = cursor.fetchall()  # Ambil semua data hasil query
       cursor.close()  # Tutup cursor

       month_dict = {month: 0 for month in
                     ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
                      "Oktober", "November", "Desember"]}  # Inisialisasi dictionary untuk semua bulan
       for bulan, nominal in data:
           month_dict[bulan] = nominal  # Isi dictionary dengan data pemasukan

       return list(month_dict.keys()), list(month_dict.values())  # Kembalikan list bulan dan nominal pemasukan

   def fetch_pengeluaran_per_month(self):
       cursor = cn.cursor()  # Buat cursor untuk eksekusi query
       query = f"SELECT bulan, SUM(nominal) FROM pengeluaran WHERE user_id = {self.user_id} GROUP BY bulan ORDER BY FIELD(bulan, 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember')"  # Query untuk pengeluaran per bulan
       cursor.execute(query)  # Eksekusi query
       data = cursor.fetchall()  # Ambil semua data hasil query
       cursor.close()  # Tutup cursor

       month_dict = {month: 0 for month in
                     ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
                      "Oktober", "November", "Desember"]}  # Inisialisasi dictionary untuk semua bulan
       for bulan, nominal in data:
           month_dict[bulan] = nominal  # Isi dictionary dengan data pengeluaran

       return list(month_dict.keys()), list(month_dict.values())  # Kembalikan list bulan dan nominal pengeluaran

def show_dashboard(self):
    # Menghancurkan semua widget yang ada di dalam root
    for widget in self.root.winfo_children():
        widget.destroy()
    
    # Mengatur grid row dan column pada root
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)

    # Fungsi untuk menampilkan halaman dashboard
    def show_dashboard_page(event=None):
        self.show_dashboard()

    # Fungsi untuk menampilkan halaman pencatatan
    def show_pencatatan_page(event=None):
        self.show_Pencatatan()

    # Fungsi untuk menampilkan halaman info
    def show_info_page(event=None):
        self.show_Info()

    # Fungsi untuk menampilkan halaman akun
    def show_akun_page(event=None):
        self.show_Akun()

    # Fungsi untuk memperbarui data keuangan berdasarkan bulan yang dipilih
    def update_data_for_month(selected_month):
        if selected_month == "Semua":
            month_value = None
        else:
            month_value = selected_month

        pemasukan, pengeluaran, sisa_uang = self.get_financial_data(month=month_value)
        formatted_pemasukan = format_rupiah(pemasukan)
        formatted_pengeluaran = format_rupiah(pengeluaran)
        formatted_sisa = format_rupiah(sisa_uang)

        nominal_pemasukan_label.configure(text=f"{formatted_pemasukan}")
        nominal_pengeluaran_label.configure(text=f"{formatted_pengeluaran}")
        sisa_label.configure(text=f"{formatted_sisa}")

    # Fungsi untuk memformat angka menjadi format rupiah
    def format_rupiah(amount):
        return f"Rp{int(amount):,}".replace(',', '.')

    # Membuat frame kontainer
    container_frame = ctk.CTkFrame(self.root, fg_color='white', corner_radius=0)
    container_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Membuat frame sebelah kiri
    left_frame = ctk.CTkFrame(container_frame, width=60, fg_color='white', corner_radius=0)
    left_frame.place(relx=0, rely=0, relwidth=0.06, relheight=1)

    # Membuat frame atas
    top_frame = ctk.CTkFrame(container_frame, height=50, fg_color='white', corner_radius=0)
    top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.08)

    # Menambahkan gambar dan teks di frame atas
    img_path = "img1.PNG"
    img = Image.open(img_path)
    img = img.resize((50, 50), Image.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(48, 48))

    img_label = ctk.CTkLabel(top_frame, image=ctk_img, text="")
    img_label.place(relx=0.005, rely=0.12)

    text_label = ctk.CTkLabel(top_frame, text="MY FINANCE", font=("Arial", 16, 'bold'), text_color='orange')
    text_label.place(relx=0.06, rely=0.27)

    # Menambahkan gambar dan teks di frame sebelah kiri (Dashboard)
    img_path = "img3.PNG"
    img = Image.open(img_path)
    img = img.resize((100, 100), Image.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(38, 38))

    img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="", fg_color=None)
    img_label.place(relx=0.18, rely=0.35)
    text_label = ctk.CTkLabel(left_frame, text="Dashboard", font=("Arial", 8), text_color='gray', fg_color=None)
    text_label.place(relx=0.15, rely=0.41)
    img_label.bind("<Button-1>", show_dashboard_page)

    # Menambahkan gambar dan teks di frame sebelah kiri (Pencatatan)
    img_path = "img4.PNG"
    img = Image.open(img_path)
    img = img.resize((100, 100), Image.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(33, 33))

    img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
    img_label.place(relx=0.30, rely=0.47)
    text_label = ctk.CTkLabel(left_frame, text="Pencatatan", font=("Arial", 8), text_color='gray')
    text_label.place(relx=0.15, rely=0.53)
    img_label.bind("<Button-1>", show_pencatatan_page)

    # Menambahkan gambar dan teks di frame sebelah kiri (Info)
    img_path = "img6.png"
    img = Image.open(img_path)
    img = img.resize((100, 100), Image.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))

    img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
    img_label.place(relx=0.14, rely=0.88)
    text_label = ctk.CTkLabel(left_frame, text="Info", font=("Arial", 8), text_color='gray')
    text_label.place(relx=0.38, rely=0.94)
    img_label.bind("<Button-1>", show_info_page)

    # Menambahkan gambar dan teks di frame atas (Akun)
    img_path = "img5.png"
    img = Image.open(img_path)
    img = img.resize((100, 100), Image.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(35, 35))

    img_label = ctk.CTkLabel(top_frame, image=ctk_img, text="")
    img_label.place(relx=0.95, rely=0.15)
    text_label = ctk.CTkLabel(top_frame, text=f"Hello {self.user_name}", font=("Arial", 13), text_color='black')
    text_label.place(relx=0.88, rely=0.27)
    img_label.bind("<Button-1>", show_akun_page)

    # Menambahkan border bawah pada frame atas
    bottom_border = ctk.CTkFrame(top_frame, height=4, fg_color='#FECE8C', corner_radius=0)
    bottom_border.place(relx=0.0, rely=1.0, relwidth=1.0, anchor='sw')

    # Membuat frame utama
    main_frame = ctk.CTkFrame(container_frame, fg_color='#E5E5E5', corner_radius=0)
    main_frame.place(relx=0.06, rely=0.08, relwidth=0.94, relheight=0.92)

    # Menambahkan label untuk periode pilihan
    periode_label = ctk.CTkLabel(main_frame, text="Pilih Periode: ", font=("Arial", 14))
    periode_label.place(relx=0.05, rely=0.06)

    # Daftar bulan untuk pilihan periode
    months = ["Semua", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
              "Oktober", "November", "Desember"]
    selected_month = ctk.StringVar()
    selected_month.set(months[0])

    # Menu dropdown untuk memilih bulan
    month_menu = ctk.CTkOptionMenu(main_frame, values=months, variable=selected_month, corner_radius=20,
                                   fg_color='#FECE8C', text_color='black', button_color='orange',
                                   dropdown_fg_color='white', dropdown_hover_color='#FECE8C',
                                   button_hover_color='#E5E5E5', anchor="w", command=update_data_for_month)
    month_menu.place(relx=0.15, rely=0.06)

    # Mendapatkan data keuangan awal
    pemasukan, pengeluaran, sisa_uang = self.get_financial_data()
    formatted_pemasukan = format_rupiah(pemasukan)
    formatted_pengeluaran = format_rupiah(pengeluaran)
    formatted_sisa = format_rupiah(sisa_uang)

    # Membuat frame untuk menampilkan pemasukan
    pemasukan_frame = ctk.CTkFrame(main_frame, fg_color='white', corner_radius=10)
    pemasukan_frame.place(relx=0.05, rely=0.16, relwidth=0.285, relheight=0.22)

    img_path = "income.png"
    img = Image.open(img_path)
    img = img.resize((50, 50), Image.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
    img_label = ctk.CTkLabel(pemasukan_frame, image=ctk_img, text="")
    img_label.place(relx=0.1, rely=0.19)

    pemasukan_label = ctk.CTkLabel(pemasukan_frame, text="Total Pemasukan", font=("Arial", 16), text_color="grey")
    pemasukan_label.place(relx=0.21, rely=0.21)
    nominal_pemasukan_label = ctk.CTkLabel(pemasukan_frame, text=f"{formatted_pemasukan}", font=("Arial", 26, 'bold'))
    nominal_pemasukan_label.place(relx=0.1, rely=0.48)

    # Membuat frame untuk menampilkan pengeluaran
    pengeluaran_frame = ctk.CTkFrame(main_frame, fg_color='white', corner_radius=10)
    pengeluaran_frame.place(relx=0.355, rely=0.16, relwidth=0.285, relheight=0.22)

    img_path = "expense.png"
    img = Image.open(img_path)
    img = img.resize((50, 50), Image.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
    img_label = ctk.CTkLabel(pengeluaran_frame, image=ctk_img, text="")
    img_label.place(relx=0.1, rely=0.19)

    pengeluaran_label = ctk.CTkLabel(pengeluaran_frame, text="Total Pengeluaran", font=("Arial", 16), text_color="grey")
    pengeluaran_label.place(relx=0.21, rely=0.21)
    nominal_pengeluaran_label = ctk.CTkLabel(pengeluaran_frame, text=f"{formatted_pengeluaran}",font=("Arial", 26, 'bold'))
    nominal_pengeluaran_label.place(relx=0.1, rely=0.48)

    # Membuat frame untuk menampilkan sisa uang
    sisa_uang_frame = ctk.CTkFrame(main_frame, fg_color='white', corner_radius=10)
    sisa_uang_frame.place(relx=0.66, rely=0.16, relwidth=0.285, relheight=0.22)

    img_path = "money.png"
    img = Image.open(img_path)
    img = img.resize((50, 50), Image.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
    img_label = ctk.CTkLabel(sisa_uang_frame, image=ctk_img, text="")
    img_label.place(relx=0.1, rely=0.19)

    sisa_label = ctk.CTkLabel(sisa_uang_frame, text="Total Saldo", font=("Arial", 16), text_color="grey")
    sisa_label.place(relx=0.21, rely=0.21)
    sisa_label = ctk.CTkLabel(sisa_uang_frame, text=f"{formatted_sisa}", font=("Arial", 26, 'bold'))
    sisa_label.place(relx=0.1, rely=0.47)

    # Membuat frame untuk menampilkan performa keuangan
    performa_frame = ctk.CTkFrame(main_frame, fg_color='white', corner_radius=10)
    performa_frame.place(relx=0.05, rely=0.41, relwidth=0.285, relheight=0.52)
    self.show_pie_chart(performa_frame)
    performa_label = ctk.CTkLabel(performa_frame, text="Performa Keuangan", font=("Arial", 16), text_color="grey")
    performa_label.place(relx=0.23, rely=0.05)

    img_path = "hijau.png"
    img = Image.open(img_path)
    img = img.resize((10, 10), Image.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(10, 10))
    img_label = ctk.CTkLabel(performa_frame, image=ctk_img, text="")
    img_label.place(relx=0.12, rely=0.8)
    green_label = ctk.CTkLabel(performa_frame, text="pemasukan", font=("Arial", 10))
    green_label.place(relx=0.2, rely=0.8)

    img_path = "orange.png"
    img = Image.open(img_path)
    img = img.resize((10, 10), Image.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(10, 10))
    img_label = ctk.CTkLabel(performa_frame, image=ctk_img, text="")
    img_label.place(relx=0.59, rely=0.8)
    yellow_label = ctk.CTkLabel(performa_frame, text="pengeluaran", font=("Arial", 10))
    yellow_label.place(relx=0.67, rely=0.8)

    # Membuat frame untuk grafik pemasukan
    grafik_pemasukan_frame = ctk.CTkFrame(main_frame, fg_color='white', corner_radius=10)
    grafik_pemasukan_frame.place(relx=0.355, rely=0.41, relwidth=0.585, relheight=0.243)
    self.show_bar_chart(grafik_pemasukan_frame, 'pemasukan')

    # Membuat frame untuk grafik pengeluaran
    grafik_pengeluaran_frame = ctk.CTkFrame(main_frame, fg_color='white', corner_radius=10)
    grafik_pengeluaran_frame.place(relx=0.355, rely=0.686, relwidth=0.585, relheight=0.243)
    self.show_bar_chart(grafik_pengeluaran_frame, 'pengeluaran')

def show_pie_chart(self, frame):
    frame_id = f"chart_{len(self.frame_ids) + 1}"
    self.frame_ids[frame] = frame_id

    pemasukan_months, pemasukan_data = self.fetch_pemasukan_per_month()
    pengeluaran_months, pengeluaran_data = self.fetch_pengeluaran_per_month()

    total_pemasukan = sum(pemasukan_data)
    total_pengeluaran = sum(pengeluaran_data)

    # Menangani kasus data kosong atau nol
    if total_pemasukan == 0 and total_pengeluaran == 0:
        for widget in frame.winfo_children():
            widget.destroy()
        return

    sizes = [total_pemasukan, total_pengeluaran]
    labels = ['Pemasukan', 'Pengeluaran']
    colors = ['#97D3CB', '#FECE8C']
    explode = (0.1, 0)

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, colors=colors, startangle=140, autopct='',
                                      wedgeprops={'width': 0.4, 'edgecolor': 'w'})

    # Memperkecil ukuran teks
    for text in texts + autotexts:
        text.set_fontsize(10)

    ax.axis('equal')  # Memastikan lingkaran terlihat sempurna

    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.05, rely=0.11, relwidth=0.9, relheight=0.7)
    canvas.draw()

def show_Pencatatan(self):
    from pencatatan_tab import Pencatatan
    pencatatan = Pencatatan(self.root, user_id=self.user_id, user_name=self.user_name)
    pencatatan.show_Pencatatan()

def show_Info(self):
    from info_tab import Info
    info = Info(self.root, user_id=self.user_id, user_name=self.user_name)
    info.show_Info()

def show_Akun(self):
    from akun_tab import Akun
    akun = Akun(self.root, user_id=self.user_id, user_name=self.user_name)
    akun.show_Akun()
