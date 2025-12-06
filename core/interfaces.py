from abc import ABC, abstractmethod
from .entities import UploadedFile

class IFileRepository(ABC):
    @abstractmethod
    def list_files(self) -> list[str]:
        """Klasördeki dosyaların isimlerini listeler."""
        pass
    
    @abstractmethod
    def get_file_path(self, filename: str) -> str:
        """Dosyanın tam yolunu döner."""
        pass

class INetworkService(ABC):
    @abstractmethod
    def get_local_ip(self) -> str:
        pass
    
    @abstractmethod
    def generate_qr(self, data: str) -> str:
        pass

class IClipboardService(ABC):
    @abstractmethod
    def copy_to_system(self, text: str):
        """Metni sistem panosuna kopyalar."""
        pass

class ISecurityService(ABC):
    @abstractmethod
    def generate_pin(self) -> str:
        """Rastgele bir PIN üretir ve saklar."""
        pass

    @abstractmethod
    def verify_pin(self, input_pin: str) -> bool:
        """Girilen PIN doğru mu kontrol eder."""
        pass

    @abstractmethod
    def get_current_pin(self) -> str:
        """Mevcut PIN'i döner."""
        pass