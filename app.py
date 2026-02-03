from flask import Flask, render_template, request, send_file
from PIL import Image
from PyPDF2 import PdfMerger
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

#pdf merger
@app.route("/merge-pdf", methods=["GET", "POST"])
def merge_pdf():

    if request.method == "POST":
        files = request.files.getlist("pdfs")

        merger = PdfMerger()

        output_filename = "merged.pdf"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        for file in files:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            merger.append(path)
        
        merger.write(output_path)
        merger.close()

        return render_template("download.hmtl", filename=output_filename)
    return render_template("merge_pdf.html")

#jpg -> png
@app.route("/jpg-to-png", methods=["GET", "POST"])
def jpg_to_png():
    if request.method == "POST":
        file = request.files["image"]

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        img = Image.open(input_path)

        output_filename = "converted.png"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        img.save(output_path)

        return render_template("download.html", filename = output_filename)
    
    return render_template("jpg_to_png.html")

#png to jpg
@app.route("/png-to-jpg", methods=["GET", "POST"])
def png_to_jpg() :
    if request.method == "POST":
        file = request.files["image"]

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        img = Image.open(input_path).convert("RGB")

        output_filename = "converted.jpg"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        img.save(output_path, quality= 90)

        return render_template("download.html", filename = output_filename)
    return render_template("png_to_jpg.html")

if __name__ == "__main__":
    app.run()


