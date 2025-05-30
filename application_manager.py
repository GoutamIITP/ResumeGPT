from string import Template
import spacy
from transformers import pipeline
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize text generation pipeline (replace with Grok 3 API if available)
generator = pipeline("text-generation", model="gpt2")

nlp = spacy.load("en_core_web_sm")

def extract_keywords(job_description):
    doc = nlp(job_description)
    keywords = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and token.text.lower() in ["python", "sql", "aws", "leadership"]:
            keywords.append(token.text)
    return keywords

def tailor_resume(resume_data, job_description):
    keywords = extract_keywords(job_description)
    tailored_resume = resume_data.copy()
    # Add keywords to skills if not present
    for keyword in keywords:
        if keyword not in tailored_resume["skills"]:
            tailored_resume["skills"].append(keyword)
    return tailored_resume

def generate_cover_letter(resume_data, job):
    template = Template("""
Dear Hiring Manager,

I am excited to apply for the $job_title position at $company_name. As a professional with experience in $skills, I believe I am a strong fit for this role.

$experience_highlights

I have attached my resume for your consideration. Thank you for your time, and I look forward to discussing my qualifications further.

Best regards,
$name
    """)
    experience_highlights = " ".join(resume_data["experience"][:2])  # Use first two experience items
    return template.substitute(
        job_title=job["title"],
        company_name=job["company"],
        skills=", ".join(resume_data["skills"]),
        experience_highlights=experience_highlights,
        name=resume_data["name"]
    )

def save_resume_as_pdf(resume_data, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph(resume_data["name"], styles["Title"]))
    story.append(Paragraph(f"Email: {resume_data['email']} | Phone: {resume_data['phone']}", styles["Normal"]))
    story.append(Paragraph("Skills", styles["Heading2"]))
    story.append(Paragraph(", ".join(resume_data["skills"]), styles["Normal"]))
    story.append(Paragraph("Experience", styles["Heading2"]))
    for exp in resume_data["experience"]:
        story.append(Paragraph(exp, styles["Normal"]))
    story.append(Paragraph("Education", styles["Heading2"]))
    for edu in resume_data["education"]:
        story.append(Paragraph(edu, styles["Normal"]))
    
    doc.build(story)

def save_cover_letter_as_pdf(cover_letter, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph(cover_letter, styles["Normal"])]
    doc.build(story)

def submit_application(job_link, resume_path, cover_letter_path):
    driver = webdriver.Chrome()  # Requires ChromeDriver
    driver.get(job_link)
    time.sleep(2)  # Wait for page to load

    # Example: Fill out a form (customize based on job board)
    try:
        # Upload resume
        resume_input = driver.find_element(By.XPATH, "//input[@type='file'][contains(@name, 'resume')]")
        resume_input.send_keys(resume_path)

        # Upload cover letter
        cover_letter_input = driver.find_element(By.XPATH, "//input[@type='file'][contains(@name, 'cover_letter')]")
        cover_letter_input.send_keys(cover_letter_path)

        # Fill other fields (e.g., name, email)
        name_input = driver.find_element(By.NAME, "name")
        name_input.send_keys("John Doe")
        
        # Submit form
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error submitting application: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    submit_application("https://example.com/apply", "resumes/tailored_resume.pdf", "applications/cover_letter.pdf") 