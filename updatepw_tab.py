updatepw_tab.py
from tkinter import messagebox  # Import messagebox untuk menampilkan pesan dialog
import customtkinter as ctk  # Import modul customtkinter sebagai ctk
from PIL import Image  # Import Image dari PIL untuk memproses gambar
from database import cn  # Import variabel cn dari modul database

class UpdatePWTab:
   def __init__(self, root):
       self.root = root  # Inisialisasi root window
       self.updatepw()  # Panggil metode updatepw() saat objek dibuat

   def updatepw(self):
       for widget in self.root.winfo_children():
           widget.destroy()  # Hapus semua widget dari root window

       # Buat left_frame dengan ukuran 550x600 dan warna latar #97D3CB
       left_frame = ctk.CTkFrame(self.root, width=550, height=600, fg_color='#97D3CB', corner_radius=0)
       left_frame.grid(row=0, column=0, sticky="nsew")

       # Buat right_frame dengan ukuran 450x600 dan warna latar putih
       right_frame = ctk.CTkFrame(self.root, width=450, height=600, fg_color='white')
       right_frame.grid(row=0, column=1, sticky="nsew")

       # Label selamat datang di right_frame dengan font Roboto 20 dan warna teks putih
       welcome_label = ctk.CTkLabel(right_frame, text="Selamat Datang", font=('Roboto', 20), fg_color='white')
       welcome_label.place(relx=0.15, rely=0.15, anchor="w")

       # Label sub judul di right_frame dengan font Roboto 15 dan warna teks putih
       sub_label = ctk.CTkLabel(right_frame, text="Ubah Passwordmu di sini!", font=('Roboto', 15), text_color='grey',
                                fg_color='white')
       sub_label.place(relx=0.15, rely=0.20, anchor="w")

       # Label dan entry field untuk email dengan font Roboto 10 dan warna teks putih
       email_label = ctk.CTkLabel(right_frame, text="Email", font=('Roboto', 10), fg_color='white')
       email_label.place(relx=0.15, rely=0.28, anchor="w")
       self.email_entry = ctk.CTkEntry(right_frame, font=('Helvetica', 10), width=300, height=30,
                                       corner_radius=10, border_color="black", fg_color='white')
       self.email_entry.place(relx=0.15, rely=0.33, anchor="w")

       # Label dan entry field untuk password baru dengan font Roboto 10 dan warna teks putih
       new_password_label = ctk.CTkLabel(right_frame, text="Password Baru", font=('Roboto', 10), fg_color='white')
       new_password_label.place(relx=0.15, rely=0.38, anchor="w")
       self.new_password_entry = ctk.CTkEntry(right_frame, font=('Helvetica', 10), width=300, height=30,
                                              corner_radius=10, border_color="black", fg_color='white')
       self.new_password_entry.place(relx=0.15, rely=0.43, anchor="w")

       # Label dan entry field untuk konfirmasi password baru dengan font Roboto 10 dan warna teks putih
       new_password_confirm_label = ctk.CTkLabel(right_frame, text="Konfirmasi Password", font=('Roboto', 10),
                                                 fg_color='white')
       new_password_confirm_label.place(relx=0.15, rely=0.48, anchor="w")
       self.new_password_confirm_entry = ctk.CTkEntry(right_frame, font=('Helvetica', 10), width=300, height=30,
                                                      corner_radius=10, border_color="black", fg_color='white')
       self.new_password_confirm_entry.place(relx=0.15, rely=0.53, anchor="w")

       # Buat button_frame di right_frame untuk menempatkan tombol update password
       button_frame = ctk.CTkFrame(right_frame, fg_color='black')
       button_frame.place(relx=0.15, rely=0.63, anchor="w")

       # Tombol "Ganti Password" dengan font Helvetica 12 bold, dan warna latar #FECE8E
       updatepw_button = ctk.CTkButton(button_frame, text="Ganti Password", font=('Helvetica', 12, 'bold'),
                                       fg_color='#FECE8E', text_color='white', width=300, height=30,
                                       command=self.update_password)
       updatepw_button.pack(padx=2, pady=2)

       # Load gambar img1.PNG dan tampilkan di left_frame
       img_path = "img1.PNG"
       img = Image.open(img_path)
       img = img.resize((500, 500), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))
       img_label = ctk.CTkLabel(left_frame, image=ctk_img, fg_color='#97D3CB', text="")
       img_label.place(relx=0.5, rely=0.5, anchor="center")

       # Load gambar img2.PNG dan tampilkan di right_frame dengan event handler untuk login
       img_path = "img2.PNG"
       img = Image.open(img_path)
       img = img.resize((500, 500), Image.LANCZOS)
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(30, 30))
       img_label = ctk.CTkLabel(right_frame, image=ctk_img, text="")
       img_label.place(relx=0.05, rely=0.73, anchor="w")
       img_label.bind("<Button-1>", lambda e: self.login())

   def update_password(self):
       email = self.email_entry.get()  # Ambil nilai dari entry email
       password_baru = self.new_password_entry.get()  # Ambil nilai dari entry password baru
       konfirmasi_password_baru = self.new_password_confirm_entry.get()  # Ambil nilai dari entry konfirmasi password baru

       # Validasi untuk memastikan semua kolom terisi
       if not email or not password_baru or not konfirmasi_password_baru:
           messagebox.showerror("Error", "Semua kolom harus diisi!")
           return

       # Validasi untuk memastikan password baru dan konfirmasi password sama
       if password_baru != konfirmasi_password_baru:
           messagebox.showerror("Error", "Password baru dan konfirmasi password tidak sama!")
           return

       # Koneksi ke database dan update password
       cursor = cn.cursor()
       qry = "UPDATE data SET password = %s WHERE email = %s"
       val = (password_baru, email)
       cursor.execute(qry, val)
       cn.commit()

       # Tampilkan pesan sukses setelah password diupdate
       messagebox.showinfo("Sukses", "Password berhasil diupdate!")

       # Kosongkan input fields setelah password diupdate
       self.email_entry.delete(0, 'end')
       self.new_password_entry.delete(0, 'end')
       self.new_password_confirm_entry.delete(0, 'end')

       # Panggil metode login untuk kembali ke halaman login
       self.login()

   def login(self):
       from login_tab import LoginTab  # Import LoginTab dari modul login_tab
       for widget in self.root.winfo_children():
           widget.destroy()  # Hapus semua widget dari root window

       # Buat objek LoginTab untuk menampilkan halaman login
       self.current_tab = LoginTab(self.root)