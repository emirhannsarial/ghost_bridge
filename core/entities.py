from dataclasses import dataclass
import datetime

@dataclass
class UploadedFile:
    filename: str
    file_data: bytes  # Dosyanın ham verisi
    upload_date: datetime.datetime = datetime.datetime.now()