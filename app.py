from flask import Flask, request, jsonify, render_template
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from utils.pyq_analyzer import analyze

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Extract text from PDF
# -----------------------------
@app.route("/extract_pdf", methods=["POST"])
def extract_pdf():
    file = request.files["file"]
    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    images = convert_from_path(
        path,
        poppler_path=r"C:\poppler\Library\bin"
    )

    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)

    return jsonify({"text": text})


# -----------------------------
# Extract text from image
# -----------------------------
@app.route("/extract_image", methods=["POST"])
def extract_image():
    file = request.files["image"]
    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    img = Image.open(path)
    text = pytesseract.image_to_string(img)

    return jsonify({"text": text})


# -----------------------------
# Analyze text
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze_route():
    data = request.json

    text = data["text"]
    syllabus = data["syllabus"]

    result = analyze(text, syllabus)

    return jsonify(result)

# -----------------------------
# Analyze by Semester and Subject
# -----------------------------
@app.route("/analyze_semester", methods=["POST"])
def analyze_semester():
    import glob
    semester = request.form.get("semester")
    subject = request.form.get("subject")
    
    if "syllabus" not in request.files:
        return jsonify({"error": "Missing syllabus file"}), 400
    
    syllabus_file = request.files["syllabus"]
    
    if not semester or not subject:
        return jsonify({"error": "Missing semester or subject"}), 400

    # Parse the uploaded Syllabus File via OCR to get syllabus text
    syllabus_path = os.path.join(app.config["UPLOAD_FOLDER"], f"temp_{syllabus_file.filename}")
    syllabus_file.save(syllabus_path)
    
    syllabus_text = ""
    try:
        if syllabus_path.lower().endswith('.pdf'):
            syl_images = convert_from_path(syllabus_path, poppler_path=r"C:\poppler\Library\bin")
            for img in syl_images:
                syllabus_text += pytesseract.image_to_string(img) + "\n"
        else:
            syl_img = Image.open(syllabus_path)
            syllabus_text += pytesseract.image_to_string(syl_img)
    except Exception as e:
        print(f"Error processing syllabus: {e}")
        return jsonify({"error": "Failed to parse syllabus file."}), 500
    finally:
        if os.path.exists(syllabus_path):
            os.remove(syllabus_path)
            
    target_dir = os.path.join(app.config["UPLOAD_FOLDER"], semester, subject.strip().lower())
    
    if not os.path.isdir(target_dir):
        # Fallback raw check for folder lookup
        alt_target = os.path.join(app.config["UPLOAD_FOLDER"], semester, subject.strip())
        if os.path.isdir(alt_target):
            target_dir = alt_target
        else:
            return jsonify({"error": f"Folder for {subject} not found in {semester}."}), 404

    pdf_files = glob.glob(os.path.join(target_dir, "*.pdf"))

    if not pdf_files:
        return jsonify({"error": f"No question papers found for {subject} in {semester}."}), 404

    aggregated_text = ""

    for pdf_path in pdf_files:
        try:
            images = convert_from_path(
                pdf_path,
                poppler_path=r"C:\poppler\Library\bin"
            )
            for img in images:
                aggregated_text += pytesseract.image_to_string(img) + "\n"
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")

    if not aggregated_text.strip():
        return jsonify({"error": "Failed to extract text from papers."}), 500

    result = analyze(aggregated_text, syllabus_text)
    return jsonify(result)


# -----------------------------
# Run app (ALWAYS LAST)
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)