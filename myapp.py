import customtkinter as ctk  # Impor modul customtkinter dengan alias ctk
from PIL import Image  # Impor modul Image dari PIL untuk pengolahan gambar
from signup_tab import SignUpTab  # Impor kelas SignUpTab dari modul signup_tab

class MyApp(ctk.CTk):
   def __init__(self):
       super().__init__()  # Memanggil konstruktor dari kelas dasar ctk.CTk
       self.title("My Finance")  # Menetapkan judul jendela aplikasi
       self.geometry("1000x600")  # Menetapkan ukuran awal jendela aplikasi
       self.configure(bg='#97D3CB')  # Menetapkan warna latar belakang jendela aplikasi

       self.current_tab = None  # Menginisialisasi atribut current_tab menjadi None
       self.show_initial_screen()  # Memanggil metode untuk menampilkan layar awal

   def show_initial_screen(self):
       for widget in self.winfo_children():
           widget.destroy()  # Menghancurkan semua widget yang ada di jendela aplikasi saat ini

       frame = ctk.CTkFrame(self, fg_color='#97D3CB')  # Membuat frame dengan warna foreground tertentu
       frame.pack(fill="both", expand=True)  # Membungkus frame untuk mengisi dan memperluas dalam jendela

       img_path = "img1.PNG"  # Path menuju file gambar
       img = Image.open(img_path)  # Membuka file gambar
       img = img.resize((500, 500), Image.LANCZOS)  # Mengubah ukuran gambar menggunakan resampling Lanczos
       ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))  # Membuat gambar kustom Tkinter

       img_label = ctk.CTkLabel(frame, image=ctk_img, fg_color='#97D3CB', text="")  # Label dengan gambar kustom
       img_label.place(relx=0.5, rely=0.5, anchor="center")  # Menempatkan label di tengah frame
       img_label.bind("<Button-1>", lambda e: self.switch_to_signup())  # Mengikat peristiwa klik kiri ke metode switch_to_signup

   def switch_to_signup(self):
       self.current_tab = SignUpTab(self)  # Membuat sebuah instance SignUpTab, meneruskan self sebagai root