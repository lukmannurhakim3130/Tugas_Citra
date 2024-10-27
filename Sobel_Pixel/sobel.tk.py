import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog, Frame, messagebox
from PIL import Image, ImageTk

# Fungsi untuk memuat gambar
def load_image():
    # Membuka dialog untuk memilih file gambar
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    
    if file_path:  # Pastikan ada file yang dipilih
        # Proses gambar asli dan deteksi tepi Sobel
        original_img = cv2.imread(file_path)  # Membaca gambar
        gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)  # Mengubah gambar ke grayscale
        blurred_img = cv2.GaussianBlur(gray_img, (3, 3), 0)  # Menghaluskan gambar untuk mengurangi noise
        
        # Menghitung deteksi tepi menggunakan operator Sobel
        sobel_x = cv2.Sobel(blurred_img, cv2.CV_8U, 1, 0, ksize=5)  # Deteksi tepi dalam arah X
        sobel_y = cv2.Sobel(blurred_img, cv2.CV_8U, 0, 1, ksize=5)  # Deteksi tepi dalam arah Y
        sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)  # Menggabungkan hasil deteksi tepi

        # Tampilkan gambar pada antarmuka
        display_image(original_img, original_panel, "Original Image")  # Gambar asli
        display_image(sobel_x, sobel_x_panel, "Sobel X")  # Hasil deteksi Sobel pada sumbu X
        display_image(sobel_y, sobel_y_panel, "Sobel Y")  # Hasil deteksi Sobel pada sumbu Y
        display_image(sobel_combined, sobel_combined_panel, "Sobel Combined")  # Hasil gabungan

# Fungsi untuk menampilkan gambar pada Tkinter
def display_image(img_array, panel, title="Image"):
    img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)  # Mengubah warna dari BGR ke RGB
    img_pil = Image.fromarray(img_rgb)  # Mengubah array gambar menjadi format PIL
    img_tk = ImageTk.PhotoImage(img_pil)  # Mengubah gambar PIL menjadi format yang dapat digunakan Tkinter

    # Update label panel dan gambar
    panel.config(image=img_tk)  # Menampilkan gambar di panel
    panel.image = img_tk  # Menyimpan referensi gambar
    panel.title.config(text=title)  # Mengupdate judul panel

    # Bind event klik untuk menampilkan ketetanggaan piksel
    panel.bind("<Button-1>", lambda event: show_pixel_adjacency(event, img_array))  # Mengikat event klik untuk menampilkan ketetanggaan

def show_pixel_adjacency(event, img_array):
    """Menampilkan ketetanggaan piksel berdasarkan koordinat yang diklik"""
    # Ambil koordinat klik
    x, y = event.x, event.y  # Mendapatkan koordinat dari event klik

    # Pastikan koordinat tidak keluar dari batas gambar
    if x < 0 or x >= img_array.shape[1] or y < 0 or y >= img_array.shape[0]:
        messagebox.showerror("Error", "Koordinat di luar batas gambar!")  # Menampilkan error jika koordinat di luar batas
        return

    # Ambil nilai piksel di posisi yang diklik
    pixel_value = img_array[y, x]  # Mendapatkan nilai piksel dari gambar
    adjacency_info = []  # Daftar untuk menyimpan informasi ketetanggaan

    # Menghitung ketetanggaan piksel (8 tetangga)
    for dy in [-1, 0, 1]:  # Melakukan iterasi untuk setiap piksel tetangga
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue  # Lewati piksel pusat
            nx, ny = x + dx, y + dy  # Koordinat piksel tetangga
            
            # Pastikan piksel tetangga ada dalam batas gambar
            if 0 <= nx < img_array.shape[1] and 0 <= ny < img_array.shape[0]:
                adjacency_info.append((nx, ny, img_array[ny, nx]))  # Menambahkan informasi piksel tetangga

    # Tampilkan informasi ketetanggaan
    adjacency_str = "\n".join([f"({nx}, {ny}): {value}" for (nx, ny, value) in adjacency_info])  # Membuat string untuk ditampilkan
    messagebox.showinfo("Ketetanggaan Piksel", f"Nilai Piksel: {pixel_value}\n\nKetetanggaan:\n{adjacency_str}")  # Menampilkan informasi

# Fungsi untuk membuat panel gambar dan label judul
def create_image_panel(parent, row, col):
    title_label = Label(parent, text="", font=("Helvetica", 10))  # Membuat label untuk judul gambar
    title_label.grid(row=row, column=col, pady=5)  # Menempatkan label di grid
    
    image_panel = Label(parent)  # Membuat panel untuk gambar
    image_panel.grid(row=row+1, column=col, padx=10, pady=10)  # Menempatkan panel di grid
    
    # Menyimpan label judul di dalam panel untuk akses lebih mudah
    image_panel.title = title_label  # Menyimpan referensi label judul di dalam panel
    return image_panel

# Setup Tkinter
root = Tk()  # Membuat instance Tkinter
root.title("Sobel Edge Detection")  # Menetapkan judul jendela

# Membuat panel-panel gambar
original_panel = create_image_panel(root, 0, 0)  # Panel untuk gambar asli
sobel_x_panel = create_image_panel(root, 0, 1)  # Panel untuk hasil Sobel X
sobel_y_panel = create_image_panel(root, 0, 2)  # Panel untuk hasil Sobel Y
sobel_combined_panel = create_image_panel(root, 2, 1)  # Panel untuk hasil gabungan

# Tambahkan pemisah untuk memperjelas tata letak
separator = Frame(root, height=2, bd=1, relief="sunken")  # Membuat pemisah
separator.grid(row=4, column=0, columnspan=3, sticky="we", pady=15)  # Menempatkan pemisah di grid

# Tombol untuk memuat gambar, dipisahkan dengan `separator`
load_btn = Button(root, text="Load Image", command=load_image, font=("Helvetica", 12, "bold"))  # Membuat tombol untuk memuat gambar
load_btn.grid(row=5, column=1, pady=15)  # Menempatkan tombol di grid

# Memulai loop utama Tkinter
root.mainloop()
