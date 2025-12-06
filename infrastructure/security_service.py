import random
from core.interfaces import ISecurityService

class PinSecurityService(ISecurityService):
    def __init__(self):
        self._pin = ""

    def generate_pin(self) -> str:
        # 1000 ile 9999 arasında rastgele sayı üret
        self._pin = str(random.randint(1000, 9999))
        return self._pin

    def verify_pin(self, input_pin: str) -> bool:
        return input_pin == self._pin

    def get_current_pin(self) -> str:
        return self._pin