from flask import Flask, render_template, request
from resume_parser import extract_text
from skill_db import roles
import os

app = Flask(__name__)

# Get current project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create uploads folder path
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Create uploads folder automatically if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # Check if file uploaded
    if "resume" not in request.files:
        return "No file uploaded!"

    resume = request.files["resume"]

    if resume.filename == "":
        return "Please select a file!"

    role = request.form["role"]

    # Save uploaded file
    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume.filename
    )

    resume.save(filepath)

    # Extract text from PDF
    text = extract_text(filepath)

    required_skills = roles[role]

    found_skills = []

    for skill in required_skills:
        if skill.lower() in text:
            found_skills.append(skill)

    missing_skills = list(
        set(required_skills) - set(found_skills)
    )

    score = int(
        (len(found_skills) /
         len(required_skills)) * 100
    )

    return render_template(
        "result.html",
        score=score,
        found=found_skills,
        missing=missing_skills,
        role=role
    )


if __name__ == "__main__":
    app.run(debug=True)