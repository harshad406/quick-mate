from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

#home Page
@app.route("/")
def home():
    return render_template("index.html")

#Image compressor page
@app.route("/compress", methods=["GET", "POST"])
def compress():
    if request.method == "POST":
        file = request.files["image"]

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_filename = "compressed_" + file.filename
        output_path = os.path.join(OUTPUT_FOLDER, "compressed_" + file.filename)

        file.save(input_path)

        img = Image.open(input_path)
        img.save(output_path, optimize=True, quality=40)

        return render_template("download.html", filename = output_filename)
    
    
    return render_template("compress.html")


#Download page
@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run()