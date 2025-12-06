import customtkinter as ctk
from PIL import Image
import os
import shutil
import webbrowser
from tkinter import filedialog

class MainWindow(ctk.CTk):
    def __init__(self, qr_path, server_url, config_service, pin_code, network_service, qr_callback): 
        super().__init__()
        self.config_service = config_service # <--- Config Servisi eklendi
        self.save_path = config_service.get("download_folder") # <--- Config'den oku
        self.network_service = network_service
        self.qr_callback = qr_callback
        self.local_url = server_url
        self.donation_url = "https://www.buymeacoffee.com/senin_kullanici_adin"

        self.title("Ghost Bridge 👻")
        self.geometry("800x650") # Biraz daha büyüttük
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- LEFT FRAME ---
        self.left_frame = ctk.CTkFrame(self, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nswe")
        
        self.qr_label = ctk.CTkLabel(self.left_frame, text="")
        self.qr_label.pack(pady=(30, 10))
        self.update_qr_image(qr_path)

        self.lbl_scan = ctk.CTkLabel(self.left_frame, text="Scan to Connect", font=("Roboto", 16))
        self.lbl_scan.pack()

        # PIN AREA
        pin_frame = ctk.CTkFrame(self.left_frame, fg_color="#333", corner_radius=10)
        pin_frame.pack(pady=20, padx=40, fill="x")
        ctk.CTkLabel(pin_frame, text="SECRET PIN", font=("Arial", 10), text_color="gray").pack(pady=(5,0))
        ctk.CTkLabel(pin_frame, text=pin_code, font=("Roboto", 40, "bold"), text_color="#2CC985").pack(pady=(0,5))

        self.lbl_url = ctk.CTkLabel(self.left_frame, text=server_url, text_color="gray", font=("Arial", 10))
        self.lbl_url.pack(side="bottom", pady=10)

        # --- RIGHT FRAME ---
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        ctk.CTkLabel(self.right_frame, text="Control Center", font=("Roboto", 18)).pack(anchor="w", pady=(10, 10))

        # Tunnel Switch
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self.right_frame, text="Global Access (Internet)", command=self.toggle_tunnel,
                                    variable=self.switch_var, onvalue="on", offvalue="off", progress_color="#e67e22")
        self.switch.pack(anchor="w", pady=(0, 15))

        # Log Box
        self.log_box = ctk.CTkTextbox(self.right_frame, width=300, height=150)
        self.log_box.pack(fill="both", expand=True)
        folder_name = os.path.basename(self.save_path)
        self.log_box.insert("0.0", f"🚀 System Ready.\n📂 Folder: {folder_name}\n----------------------\n")
        self.log_box.configure(state="disabled")

        # --- KLASÖR YÖNETİMİ BUTONLARI ---
        
        # 1. Klasörü Değiştir (YENİ)
        self.btn_change_folder = ctk.CTkButton(self.right_frame, text="Change Save Folder ⚙️", fg_color="#555", hover_color="#444", command=self.change_save_folder)
        self.btn_change_folder.pack(pady=(10, 5), fill="x")

        # 2. Klasörü Aç
        self.btn_open_folder = ctk.CTkButton(self.right_frame, text="Open Folder 📂", command=lambda: os.startfile(self.save_path))
        self.btn_open_folder.pack(pady=5, fill="x")

        # 3. Dosya Paylaş
        self.btn_add_file = ctk.CTkButton(self.right_frame, text="Share File 📤", fg_color="#2CC985", hover_color="#229e68", command=self.select_file)
        self.btn_add_file.pack(pady=5, fill="x")

        # Donation
        self.btn_donate = ctk.CTkButton(self.right_frame, text="☕ Buy me a Coffee", 
                                        fg_color="#FFDD00", text_color="black", hover_color="#e6c700",
                                        font=("Arial", 13, "bold"),
                                        command=self.open_donation_link)
        self.btn_donate.pack(side="bottom", pady=10, fill="x")

    def change_save_folder(self):
        """Kullanıcıya yeni klasör seçtirir ve kaydeder"""
        new_folder = filedialog.askdirectory()
        if new_folder:
            self.save_path = new_folder
            self.config_service.set("download_folder", new_folder) # Config'e kaydet
            self.add_log(f"✅ Folder Changed: {os.path.basename(new_folder)}")
            # Not: Sunucunun da bu değişikliği bilmesi için yeniden başlatılması gerekebilir 
            # veya server tarafında her işlemde config okunmalı.
            self.add_log("⚠️ Restart app to apply for incoming files.")

    def toggle_tunnel(self):
        if self.switch_var.get() == "on":
            self.add_log("🌍 Starting Global Tunnel...")
            try:
                # Ngrok'a hangi portu kullanacağımızı (self.local_url'den çekip) söylememiz lazım ama
                # Basitlik için main.py'den port bilgisini alabiliriz veya 
                # Tunneling yaparken servisin kendi portunu bilmesini sağlayabiliriz.
                # Şimdilik port sabit değil, servisin bilmesi lazım.
                # (Aşağıdaki Main.py adımında bunu çözeceğiz)
                pass 
            except Exception as e:
                self.add_log(f"❌ Error: {str(e)}")
                self.switch.deselect()
        # ... (Diğer fonksiyonlar aynı) ...

    # DİĞER FONKSİYONLAR (open_donation_link, update_qr_image, select_file, add_log) AYNI KALSIN
    def open_donation_link(self):
        webbrowser.open_new(self.donation_url)

    def update_qr_image(self, path):
        if os.path.exists(path):
            img = ctk.CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=(180, 180))
            self.qr_label.configure(image=img)
            self.qr_label.image = img

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                filename = os.path.basename(file_path)
                destination = os.path.join(self.save_path, filename)
                shutil.copy2(file_path, destination)
                self.add_log(f"➕ File Shared: {filename}")
            except Exception as e:
                self.add_log(f"❌ Error: {str(e)}")

    def add_log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")