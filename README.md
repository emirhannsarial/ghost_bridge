<div align="center">
  <h1>Ghost Bridge 👻</h1>
  <p>
    <strong>Seamless File Transfer Between PC & Mobile.</strong>
    <br>
    No Apps. No Cables. No Internet Required.
  </p>

  <p>
    <a href="#features">Features</a> •
    <a href="#how-to-use">How To Use</a> •
    <a href="#installation-developers">For Developers</a> •
    <a href="#support">Support</a>
  </p>

  ![Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
  ![Platform](https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge&logo=windows)
</div>

---

## 🚀 What is Ghost Bridge?

**Ghost Bridge** is a lightweight desktop tool that creates an instant, secure bridge between your Windows PC and any smartphone (iOS/Android).

Unlike other solutions, **you do not need to install any app on your phone.** Just scan the QR code, and you are connected via your mobile browser.

It solves the *"How do I get this file/text to my PC quickly?"* problem once and for all.

## ✨ Key Features

* **📱 Zero-App Policy:** The phone side runs entirely in the browser. No Play Store/App Store downloads required.
* **⚡ Blazing Fast:** Uses your local Wi-Fi network. Transfer gigabytes in seconds.
* **📋 Universal Clipboard:** Copy text on your phone, paste it on your PC (and vice versa).
* **🔒 Secure:** * Files stay on your local network (Privacy First).
    * Protected by a random **4-digit PIN** for every session.
* **🌍 Global Tunneling:** Need to transfer files over 4G/LTE? Switch on "Global Access" to create a secure tunnel via Ngrok.
* **📂 Bi-Directional:** Send files from Phone to PC, or download files from PC to Phone.

---

## 📸 Screenshots

<img width="801" height="674" alt="image" src="https://github.com/user-attachments/assets/d88ee301-1d90-40a4-b184-bbedbecaa786" />
<img width="1224" height="1001" alt="image" src="https://github.com/user-attachments/assets/e85cbca8-2c1e-4487-9215-7fe3472af8b2" />
<img width="1228" height="1006" alt="image" src="https://github.com/user-attachments/assets/d1fe3860-bd18-4108-a2ed-f3160dda6ac5" />


---


## 🛠 Installation (For Developers)

If you want to run the source code or contribute:

### Prerequisites
* Python 3.10+
* pip

### Steps

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/emirhannsarial/ghost_bridge.git](https://github.com/emirhannsarial/ghost_bridge.git)
    cd GhostBridge
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Dependencies: customtkinter, flask, pyngrok, qrcode, pillow, pyinstaller)*

3.  **Run the App**
    ```bash
    python main.py
    ```

### Building the .exe
To create the executable file yourself:
```bash
python -m PyInstaller --noconsole --onefile --name="GhostBridge" --icon="icon.ico" --add-data "static;static" --collect-all customtkinter --collect-all pyngrok main.py


