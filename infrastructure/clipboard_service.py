# infrastructure/clipboard_service.py
import pyperclip
from core.interfaces import IClipboardService

class SystemClipboardService(IClipboardService):
    def copy_to_system(self, text: str):
        pyperclip.copy(text)