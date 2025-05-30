from flask import Flask, request, render_template
from resume_parser import parse_resume
from job_scraper import scrape_jobs
from application_manager import tailor_resume, generate_cover_letter, submit_application
from scheduler import schedule_interview
import os

app = Flask(__name__)
UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume_file = request.files["resume"]
        resume_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
        resume_file.save(resume_path)

        resume_data = parse_resume(resume_path)
        job_role = request.form["job_role"]
        location = request.form["location"]

        jobs = scrape_jobs()

        for job in jobs[:2]:  # Limit to 2 for testing
            tailored_resume = tailor_resume(resume_data, job["description"])
            cover_letter = generate_cover_letter(tailored_resume, job)
            resume_pdf = f"applications/tailored_resume_{job['title']}.pdf"
            cover_letter_pdf = f"applications/cover_letter_{job['title']}.pdf"
            submit_application(job["link"], resume_pdf, cover_letter_pdf)

        return render_template("index.html", message="Applications submitted!")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True) 