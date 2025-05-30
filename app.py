import os
from flask import Flask, request, render_template, redirect, url_for
# from resume_parser import parse_resume # Make sure resume_parser.py is in the same directory

# Import parse_resume from the local file
from resume_parser import parse_resume
from job_scraper import scrape_jobs
from application_manager import tailor_resume, generate_cover_letter, submit_application
from scheduler import schedule_interview
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "resume" not in request.files:
            return render_template("index.html", error="No file uploaded")
        
        resume_file = request.files["resume"]
        if resume_file.filename == "":
            return render_template("index.html", error="No file selected")
        
        if not resume_file.filename.endswith((".pdf", ".docx")):
            return render_template("index.html", error="Invalid file format. Please upload a PDF or Word document")
        
        if not request.form.get("consent"):
            return render_template("index.html", error="Please provide consent to process your resume")
        
        resume_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
        resume_file.save(resume_path)
        
        try:
            resume_data = parse_resume(resume_path)
            os.remove(resume_path)
            if not resume_data:
                return render_template("index.html", error="Failed to parse resume")
            return render_template("results.html", resume_data=resume_data)
        except Exception as e:
            if os.path.exists(resume_path):
                os.remove(resume_path)
            return render_template("index.html", error=f"Error processing resume: {str(e)}")
    
    return render_template("index.html", error=None)

@app.route("/clear", methods=["POST"])
def clear():
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER)
    return render_template("index.html", error=None)

if __name__ == "__main__":
    app.run(debug=True) 