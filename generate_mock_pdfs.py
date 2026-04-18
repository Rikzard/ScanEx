from PIL import Image, ImageDraw
import os

os.makedirs("uploads/semester_3/dbms", exist_ok=True)

def create_pdf(filename, lines):
    img = Image.new('RGB', (800, 1000), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    y = 50
    for line in lines:
        d.text((50, y), line, fill=(0,0,0))
        y += 40
    img.save(filename, "PDF", resolution=100.0)

create_pdf("uploads/semester_3/dbms/paper1.pdf", [
    "DBMS Question Paper 2025",
    "What is DBMS?",
    "Explain normalization in detail.",
    "Define ACID properties."
])

create_pdf("uploads/semester_3/dbms/paper2.pdf", [
    "DBMS Mid-Term Paper",
    "What is DBMS?",
    "Describe functional dependency.",
    "Explain normalization in DBMS.",
])

create_pdf("uploads/dummy_syllabus.pdf", [
    "Syllabus for DBMS",
    "DBMS",
    "normalization",
    "ACID",
    "functional dependency"
])

print("Dummy files generated successfully!")
