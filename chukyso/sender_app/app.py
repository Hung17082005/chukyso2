from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os, requests

app = Flask(__name__)
KEY_DIR = "keys"
SIGNED_DIR = "signed"
os.makedirs(KEY_DIR, exist_ok=True)
os.makedirs(SIGNED_DIR, exist_ok=True)

# Tạo hoặc load khóa RSA
priv_path = os.path.join(KEY_DIR, "private.pem")
pub_path = os.path.join(KEY_DIR, "public.pem")
if not os.path.exists(priv_path):
    key = RSA.generate(2048)
    with open(priv_path, "wb") as f:
        f.write(key.export_key())
    with open(pub_path, "wb") as f:
        f.write(key.publickey().export_key())

with open(priv_path, "rb") as f:
    private_key = RSA.import_key(f.read())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign", methods=["POST"])
def sign():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    data = file.read()

    file_path = os.path.join(SIGNED_DIR, filename)
    sig_path = os.path.join(SIGNED_DIR, filename + ".sig")

    with open(file_path, "wb") as f:
        f.write(data)

    h = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(h)
    with open(sig_path, "wb") as f:
        f.write(signature)

    return render_template("index.html", message="✅ Đã ký thành công!", filename=filename)

@app.route("/send", methods=["POST"])
def send():
    filename = request.form["filename"]
    files = {
        'file': open(os.path.join(SIGNED_DIR, filename), 'rb'),
        'signature': open(os.path.join(SIGNED_DIR, filename + ".sig"), 'rb'),
        'public_key': open(os.path.join(KEY_DIR, "public.pem"), 'rb')
    }

    try:
        r = requests.post("http://localhost:5001/receive", files=files)
        if r.status_code == 200:
            return render_template("index.html", message="📨 Đã gửi file thành công!", filename=None)
        else:
            return render_template("index.html", message="❌ Gửi thất bại!", filename=filename)
    except Exception as e:
        return render_template("index.html", message="🚫 Lỗi khi gửi: " + str(e), filename=filename)

if __name__ == "__main__":
    app.run(port=5000)
