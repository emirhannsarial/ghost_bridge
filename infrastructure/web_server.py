from flask import Flask, request, render_template_string, jsonify, send_file, session, redirect, url_for
import threading
import os
import sys
import urllib.parse # Dosya isimlerini decode etmek için

# EXE İÇİN DOSYA BULUCU
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_html(filename):
    """HTML dosyasını static klasöründen okur"""
    path = resource_path(os.path.join('static', filename))
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

class FlaskServer:
    def __init__(self, upload_use_case, clipboard_use_case, list_files_use_case, file_repo, security_service, log_callback=None):
        self.app = Flask(__name__)
        self.app.secret_key = "GHOST_BRIDGE_SECRET"
        
        self.upload_use_case = upload_use_case
        self.clipboard_use_case = clipboard_use_case
        self.list_files_use_case = list_files_use_case
        self.file_repo = file_repo
        self.security_service = security_service
        self.log_callback = log_callback
        self.server_thread = None
        self.setup_routes()

    def check_auth(self):
        return session.get('authenticated') == True

    def setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                pin = request.form.get('pin')
                if self.security_service.verify_pin(pin):
                    session['authenticated'] = True
                    return render_template_string(load_html('dashboard.html'))
                else:
                    return render_template_string(load_html('login.html'), error=True)
            
            if self.check_auth():
                return render_template_string(load_html('dashboard.html'))
            return render_template_string(load_html('login.html'), error=False)

        @self.app.route('/logout')
        def logout():
            session.pop('authenticated', None)
            return redirect(url_for('index'))

        @self.app.route('/upload', methods=['POST'])
        def upload_file():
            if not self.check_auth(): return "Unauthorized", 401
            if 'file' not in request.files: return "No file", 400
            file = request.files['file']
            if file.filename == '': return "No selection", 400
            try:
                self.upload_use_case.execute(file.filename, file.read())
                if self.log_callback: self.log_callback(f"📥 Received: {file.filename}")
                return f"<script>alert('Sent!'); window.location.href='/';</script>"
            except Exception as e: return str(e), 500

        @self.app.route('/clipboard', methods=['POST'])
        def clipboard():
            if not self.check_auth(): return jsonify({"error"}), 401
            data = request.json
            self.clipboard_use_case.execute(data.get('text', ''))
            if self.log_callback: self.log_callback(f"📋 Clipboard synced.")
            return jsonify({"status": "success"})

        @self.app.route('/files', methods=['GET'])
        def list_files():
            if not self.check_auth(): return jsonify({"error"}), 401
            files = self.list_files_use_case.execute()
            return jsonify({"files": files})

        @self.app.route('/download/<path:filename>', methods=['GET'])
        def download_file(filename):
            if not self.check_auth(): return "Unauthorized", 401
            try:
                # URL decode yap (Örn: "tatil%20fotosu.jpg" -> "tatil fotosu.jpg")
                decoded_name = urllib.parse.unquote(filename)
                path = self.file_repo.get_file_path(decoded_name)
                return send_file(path, as_attachment=True)
            except Exception as e:
                return str(e), 404

    def run(self, host, port):
        self.server_thread = threading.Thread(target=lambda: self.app.run(host=host, port=port, use_reloader=False), daemon=True)
        self.server_thread.start()