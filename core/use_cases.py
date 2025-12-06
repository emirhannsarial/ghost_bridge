from .entities import UploadedFile
from .interfaces import IFileRepository, IClipboardService

# 1. Dosya Yükleme Mantığı
class UploadFileUseCase:
    def __init__(self, file_repository: IFileRepository):
        self.repository = file_repository # Dependency Injection

    def execute(self, filename: str, file_data: bytes) -> dict:
        if not file_data:
            raise ValueError("Dosya içeriği boş olamaz.")
        
        new_file = UploadedFile(filename=filename, file_data=file_data)
        saved_path = self.repository.save(new_file)
        
        return {
            "status": "success",
            "message": f"{filename} başarıyla alındı.",
            "path": saved_path
        }

# 2. Pano (Clipboard) Mantığı
class UpdateClipboardUseCase:
    def __init__(self, clipboard_service: IClipboardService):
        self.clipboard_service = clipboard_service

    def execute(self, text: str) -> dict:
        if not text:
            raise ValueError("Metin boş olamaz")
        
        self.clipboard_service.copy_to_system(text)
        
        return {
            "status": "success",
            "message": "Metin PC panosuna kopyalandı"
        }
    
class ListFilesUseCase:
    def __init__(self, file_repository: IFileRepository):
        self.repository = file_repository

    def execute(self) -> list[str]:
        return self.repository.list_files()