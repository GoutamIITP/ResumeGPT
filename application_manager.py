from transformers import pipeline
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize text generation pipeline (replace with Grok 3 API if available)
# Using a smaller model for demonstration purposes
generator = pipeline("text-generation", model="gpt2", max_new_tokens=150)

def extract_keywords(job_description):
    if not job_description:
        return []
    prompt = f"Extract key skills and qualifications from this job description: {job_description}"
    try:
        # Adjusting parameters for potentially better keyword extraction within the model's capabilities
        response = generator(prompt, num_return_sequences=1, do_sample=True, top_p=0.95, top_k=50)[0]["generated_text"]
        # Basic keyword extraction - can be improved with more advanced techniques
        keywords = [word.strip('.,!?;:"\'').lower() for word in response.split() if len(word) > 2]
        # Filter for some common tech/business keywords as an example
        common_keywords = ["python", "sql", "aws", "leadership", "javascript", "react", "data", "engineer", "manager", "analyst"]
        extracted = [k for k in keywords if k in common_keywords]
        return list(set(extracted))
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

def tailor_resume(resume_data, job_description):
    if not resume_data:
        return resume_data # Return original if no data

    keywords = extract_keywords(job_description)
    tailored_resume = resume_data.copy()
    
    # Add keywords to skills if they are not already present
    current_skills_lower = [s.lower() for s in tailored_resume.get("skills", [])]
    added_keywords = []
    for keyword in keywords:
        if keyword not in current_skills_lower:
            # Capitalize the first letter for better presentation
            tailored_resume.setdefault("skills", []).append(keyword.capitalize())
            added_keywords.append(keyword.capitalize())
            
    if added_keywords:
        print(f"Added keywords to resume skills: {', '.join(added_keywords)}")

    # Note: More sophisticated tailoring would involve rewriting sections
    # This basic implementation only adds keywords to the skills list
    
    return tailored_resume

def generate_cover_letter(resume_data, job):
    if not resume_data or not job:
        return ""
        
    name = resume_data.get("name", "Candidate")
    skills = ", ".join(resume_data.get("skills", []))
    experience = ". ".join(resume_data.get("experience", [])[:2]) # Use up to first 2 experience entries
    job_title = job.get("title", "the position")
    company_name = job.get("company", "the company")
    
    prompt = f"""
    Write a concise, professional cover letter for {name} applying for a {job_title} position at {company_name}. 
    Highlight relevant skills such as {skills}.
    Mention experience like: {experience}.
    Keep it brief and to the point.
    """
    
    try:
        cover_letter = generator(prompt, num_return_sequences=1, max_new_tokens=200, do_sample=True, top_p=0.95, top_k=50)[0]["generated_text"]
        # Basic post-processing to clean up the generated text
        cover_letter = cover_letter.strip()
        # Remove the original prompt if the model included it
        if cover_letter.startswith(prompt.strip()):
             cover_letter = cover_letter[len(prompt.strip()):].strip()
        return cover_letter
    except Exception as e:
        print(f"Error generating cover letter: {e}")
        return ""

def save_resume_as_pdf(resume_data, output_path):
    if not resume_data:
        print("No resume data to save.")
        return

    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph(resume_data.get("name", ""), styles["Title"]))
    story.append(Paragraph(f"Email: {resume_data.get('email', '')} | Phone: {resume_data.get('phone', '')}", styles["Normal"]))
    story.append(Spacer(1, 12)) # Add some space
    
    skills = resume_data.get("skills")
    if skills:
        story.append(Paragraph("Skills", styles["Heading2"]))
        story.append(Paragraph(", ".join(skills), styles["Normal"]))
        story.append(Spacer(1, 12))
        
    experience = resume_data.get("experience")
    if experience:
        story.append(Paragraph("Experience", styles["Heading2"]))
        for exp in experience:
            story.append(Paragraph(exp, styles["Normal"]))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))
        
    education = resume_data.get("education")
    if education:
        story.append(Paragraph("Education", styles["Heading2"]))
        for edu in education:
            story.append(Paragraph(edu, styles["Normal"]))
            story.append(Spacer(1, 6))
            
    try:
        doc.build(story)
        print(f"Resume saved to {output_path}")
    except Exception as e:
        print(f"Error saving resume PDF: {e}")

def save_cover_letter_as_pdf(cover_letter, output_path):
    if not cover_letter:
        print("No cover letter content to save.")
        return
        
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph(cover_letter, styles["Normal"])]
    
    try:
        doc.build(story)
        print(f"Cover letter saved to {output_path}")
    except Exception as e:
        print(f"Error saving cover letter PDF: {e}")

def submit_application(job_link, resume_path, cover_letter_path, resume_data):
    if not job_link or not resume_path or not resume_data:
        print("Missing required information for application submission.")
        return False
        
    print(f"Attempting to submit application for {job_link}")
    driver = None
    try:
        # Configure Chrome options for headless browsing and other preferences if needed
        # from selenium.webdriver.chrome.options import Options
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # driver = webdriver.Chrome(options=chrome_options)
        
        driver = webdriver.Chrome()
        driver.get(job_link)
        
        # Use WebDriverWait for better robustness
        wait = WebDriverWait(driver, 10) # Wait up to 10 seconds

        # Find and fill resume upload input
        # This XPath is a common pattern, but may need adjustment for specific sites
        try:
            resume_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file'][contains(@name, 'resume') or contains(@id, 'resume')]" )))
            resume_input.send_keys(os.path.abspath(resume_path))
            print("Uploaded resume.")
        except Exception as e:
            print(f"Could not find or interact with resume upload element: {e}")
            # Decide whether to continue or return False if resume upload is critical

        # Find and fill cover letter upload input (Optional field on many forms)
        try:
            cover_letter_input = driver.find_element(By.XPATH, "//input[@type='file'][contains(@name, 'cover_letter') or contains(@id, 'cover_letter')]" ) # Using find_element, might not exist
            cover_letter_input.send_keys(os.path.abspath(cover_letter_path))
            print("Uploaded cover letter.")
        except:
            print("Cover letter upload element not found, skipping.")
            # This is fine, continue if cover letter is optional

        # Find and fill name, email fields (Basic example, adjust as needed)
        try:
            name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='name' or @id='name']" )))
            name_input.send_keys(resume_data.get("name", ""))
            print("Filled name.")
        except Exception as e:
            print(f"Could not find or interact with name input element: {e}")
            # Handle appropriately
            
        try:
            email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email' or @id='email']" )))
            email_input.send_keys(resume_data.get("email", ""))
            print("Filled email.")
        except Exception as e:
             print(f"Could not find or interact with email input element: {e}")
            # Handle appropriately
            
        # Click submit button
        # This XPath is a common pattern, but may need adjustment
        try:
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']" )))
            submit_button.click()
            print("Clicked submit button.")
            time.sleep(5) # Wait for page to potentially load after submission
            # Add checks here for submission success messages or URL changes
            return True
        except Exception as e:
            print(f"Could not find or click submit button: {e}")
            return False
            
    except Exception as e:
        print(f"An error occurred during application submission: {e}")
        return False
    finally:
        if driver:
            # driver.quit() # Uncomment in production
            pass # Keep browser open for debugging

if __name__ == "__main__":
    # Example Usage for testing
    print("Running application_manager.py test...")
    dummy_resume_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "phone": "987-654-3210",
        "skills": ["Python", "Data Analysis"],
        "experience": ["Analyzed data using Python and Pandas."],
        "education": ["MS Data Science, Another University"]
    }
    dummy_job = {"title": "Data Analyst", "company": "Data Co.", "description": "Looking for a data analyst with strong Python skills.", "link": "https://www.example.com/apply-here"}
    
    tailored_resume_data = tailor_resume(dummy_resume_data, dummy_job["description"])
    print("Tailored Resume Data:", tailored_resume_data)
    
    cover_letter_content = generate_cover_letter(tailored_resume_data, dummy_job)
    print("Generated Cover Letter:", cover_letter_content)
    
    # Create dummy directories if they don't exist for saving files
    os.makedirs("applications", exist_ok=True)
    
    resume_pdf_path = "applications/jane_doe_resume.pdf"
    cover_letter_pdf_path = "applications/jane_doe_cover_letter.pdf"
    
    save_resume_as_pdf(tailored_resume_data, resume_pdf_path)
    save_cover_letter_as_pdf(cover_letter_content, cover_letter_pdf_path)
    
    # Note: Automated submission requires a running Selenium WebDriver (e.g., chromedriver)
    # and will open a browser window. It is commented out by default.
    # submit_success = submit_application(dummy_job["link"], resume_pdf_path, cover_letter_pdf_path, tailored_resume_data)
    # print(f"Application Submission Status: {\"Successful\" if submit_success else \"Failed\"}") 