import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization

# Tạo khóa RSA (chạy 1 lần, sau đó lưu lại để dùng tiếp)
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Lưu public key ra file để gửi cho máy B
with open("public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

# Tải lên file + chữ ký
filename = "sample.txt"
with open(filename, "rb") as f:
    data = f.read()

# Ký bằng private key
signature = private_key.sign(
    data,
    padding.PKCS1v15(),
    hashes.SHA256()
)

# Gửi đến server (Máy B)
url = "http://<IP_MAY_B>:5000/receive"
files = {
    'file': (filename, data),
    'signature': ('signature.sig', signature)
}

res = requests.post(url, files=files)
print(res.text)
