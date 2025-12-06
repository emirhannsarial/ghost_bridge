# infrastructure/network_service.py
import socket
import qrcode
from pyngrok import ngrok
from core.interfaces import INetworkService

class WindowsNetworkService(INetworkService):
    def __init__(self):
        self.public_url = None
        self.tunnel = None

    def get_local_ip(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def generate_qr(self, data: str) -> str:
        qr = qrcode.make(data)
        qr_path = "connection_qr.png"
        qr.save(qr_path)
        return qr_path

    # --- YENİ: AKILLI PORT BULUCU ---
    def find_free_port(self, start_port=5000):
        """Belirtilen porttan başlayarak boş bir port bulur."""
        port = start_port
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Portu kontrol et, eğer bağlanabiliyorsa (0 dönerse) doludur.
                in_use = s.connect_ex(('localhost', port)) == 0
                
            if not in_use: # Boşsa bu portu döndür
                return port
            else: # Doluysa bir artır ve tekrar dene
                port += 1
                if port > 6000: # Sonsuz döngü koruması
                    raise Exception("Boş port bulunamadı!")

    def start_tunnel(self, port):
        if not self.tunnel:
            # Ngrok'a hangi portu tünelleyeceğini dinamik olarak veriyoruz
            self.tunnel = ngrok.connect(port)
            self.public_url = self.tunnel.public_url
        return self.public_url

    def stop_tunnel(self):
        if self.tunnel:
            ngrok.disconnect(self.public_url)
            self.tunnel = None
            self.public_url = None