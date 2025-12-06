import os
from core.interfaces import IFileRepository
from core.entities import UploadedFile

class LocalFileRepository(IFileRepository):
    def __init__(self, upload_folder="Ghost_Inbox"):
        self.upload_folder = upload_folder
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def save(self, file: UploadedFile) -> str:
        file_path = os.path.join(self.upload_folder, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file_data)
        return file_path

    def list_files(self) -> list[str]:
        # Dosyaları al
        files = [f for f in os.listdir(self.upload_folder) if os.path.isfile(os.path.join(self.upload_folder, f))]
        # Tarihe göre sırala (En yeni en üstte)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(self.upload_folder, x)), reverse=True)
        return files

    def get_file_path(self, filename: str) -> str:
        # Mutlak yol (Absolute Path) döndür ki hata olmasın
        return os.path.abspath(os.path.join(self.upload_folder, filename))