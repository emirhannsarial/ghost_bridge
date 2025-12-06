import json
import os

class ConfigService:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.default_config = {
            "download_folder": os.path.abspath("Ghost_Inbox"),
            "theme": "Dark"
        }
        self.config = self.load_config()

    def load_config(self):
        """Varsa config dosyasını yükler, yoksa varsayılanı yaratır."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return self.default_config
        else:
            return self.default_config

    def save_config(self):
        """Mevcut ayarları dosyaya yazar."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get(self, key):
        return self.config.get(key, self.default_config.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save_config()