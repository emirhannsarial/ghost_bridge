# main.py
import os
import sys
from core.use_cases import UploadFileUseCase, UpdateClipboardUseCase, ListFilesUseCase
from infrastructure.file_repository import LocalFileRepository
from infrastructure.network_service import WindowsNetworkService
from infrastructure.clipboard_service import SystemClipboardService
from infrastructure.security_service import PinSecurityService
from infrastructure.config_service import ConfigService # <--- Yeni Servis
from infrastructure.web_server import FlaskServer
from ui.main_window import MainWindow

def main():
    # 1. AYARLARI YÜKLE
    config_service = ConfigService()
    download_folder = config_service.get("download_folder")
    
    # Klasör yoksa yarat
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # 2. ALTYAPIYI HAZIRLA
    file_repo = LocalFileRepository(upload_folder=download_folder)
    network_service = WindowsNetworkService()
    clipboard_service = SystemClipboardService()
    security_service = PinSecurityService()
    
    # 3. USE CASES
    upload_uc = UploadFileUseCase(file_repository=file_repo)
    clipboard_uc = UpdateClipboardUseCase(clipboard_service=clipboard_service)
    list_files_uc = ListFilesUseCase(file_repository=file_repo)

    # 4. NETWORK (AKILLI PORT)
    local_ip = network_service.get_local_ip()
    port = network_service.find_free_port(5000) # <--- Boş port bul
    
    url = f"http://{local_ip}:{port}"
    qr_path = network_service.generate_qr(url)
    pin_code = security_service.generate_pin()

    # 5. UI BAŞLAT
    # Tunnel açarken port numarasını bilmesi için lambda fonksiyonu kullanıyoruz
    def toggle_tunnel_wrapper():
        try:
            public_url = network_service.start_tunnel(port=port) # <--- Doğru portu ver
            return public_url
        except Exception as e:
            raise e

    app = MainWindow(
        qr_path=qr_path, 
        server_url=url,
        config_service=config_service,
        pin_code=pin_code,
        network_service=network_service,
        qr_callback=lambda new_url: app.update_qr_image(network_service.generate_qr(new_url))
    )
    
    # UI içindeki switch komutunu burada override (ezme) edelim ki port bilgisini verebilelim
    # Not: UI kodunu karmaşıklaştırmamak için burada basit bir "Monkey Patch" yapıyoruz.
    orig_toggle = app.toggle_tunnel
    def patched_toggle():
        if app.switch_var.get() == "on":
            app.add_log("🌍 Starting Global Tunnel...")
            try:
                public_url = network_service.start_tunnel(port) # <--- Port burada kullanılıyor
                app.add_log(f"✅ Online: {public_url}")
                app.lbl_url.configure(text=public_url)
                app.qr_callback(public_url)
                app.is_global = True
            except Exception as e:
                app.add_log(f"❌ Error: {str(e)}")
                app.switch.deselect()
        else:
            app.add_log("🏠 Stopping Tunnel. Local only.")
            network_service.stop_tunnel()
            app.lbl_url.configure(text=app.local_url)
            app.qr_callback(app.local_url)
            app.is_global = False
    
    app.toggle_tunnel = patched_toggle # Fonksiyonu değiştir

    # 6. SERVER BAŞLAT
    server = FlaskServer(
        upload_use_case=upload_uc, 
        clipboard_use_case=clipboard_uc,
        list_files_use_case=list_files_uc,
        file_repo=file_repo,
        security_service=security_service,
        log_callback=app.add_log
    )
    server.run(host="0.0.0.0", port=port) # <--- Bulunan portta çalıştır

    print(f"Ghost Bridge Running on Port {port}... PIN: {pin_code} 👻")
    app.mainloop()

if __name__ == "__main__":
    main()