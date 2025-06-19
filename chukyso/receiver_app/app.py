from flask import send_from_directory

@app.route("/files")
def list_files():
    files = []
    for f in os.listdir(INBOX_DIR):
        if f.endswith(".sig"): continue  # chỉ hiển thị file gốc
        if f == "public.pem": continue
        files.append(f)
    return render_template("index.html", files=files)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(INBOX_DIR, filename, as_attachment=True)
