from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import os
from pathlib import Path

import certifi

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = Path.home() / "Downloads"
LOG_FILE = Path(__file__).with_name("yt-dlp.log")


@app.after_request
def add_private_network_header(response):
    response.headers['Access-Control-Allow-Private-Network'] = 'true'
    return response


@app.route('/download', methods=['POST'])
def download_video():
    data = request.json or {}
    video_url = data.get('url')

    if not video_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    try:
        DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env["SSL_CERT_FILE"] = certifi.where()
        env["REQUESTS_CA_BUNDLE"] = certifi.where()
        env["CURL_CA_BUNDLE"] = certifi.where()

        log_handle = open(LOG_FILE, "a", encoding="utf-8")
        command = [
            sys.executable, "-m", "yt_dlp",
            "--no-check-certificate",
            "-P", str(DOWNLOAD_DIR),
            "-o", "%(title)s [%(id)s].%(ext)s",
            "-f", "b/bv*+ba/b",
            video_url,
        ]
        subprocess.Popen(
            command,
            cwd=str(DOWNLOAD_DIR),
            env=env,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
        )
        return jsonify({
            "status": "success",
            "message": f"Download started in {DOWNLOAD_DIR}"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
