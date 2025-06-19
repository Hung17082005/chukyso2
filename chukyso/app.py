from flask import Flask, request
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)
UPLOAD_FOLDER = 'received'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Đọc public key từ file
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

@app.route('/receive', methods=['POST'])
def receive():
    file = request.files['file']
    signature = request.files['signature'].read()
    content = file.read()
    file.seek(0)

    # Lưu file
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    # Xác minh chữ ký RSA
    try:
        public_key.verify(
            signature,
            content,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return "✅ Chữ ký xác thực đúng! File hợp lệ."
    except Exception as e:
        return f"❌ Sai chữ ký hoặc file bị chỉnh sửa: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
