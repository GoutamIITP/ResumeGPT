import pdfplumber
import spacy
import re

# Initialize NER pipeline (replace with Grok 3 API if available)
nlp = spacy.load("en_core_web_sm")

def parse_resume(file_path):
    # Extract text from PDF
    with pdfplumber.open(file_path) as pdf:
        text = "".join(page.extract_text() for page in pdf.pages)

    # Process text with spaCy
    doc = nlp(text)
    
    # Extract entities
    name = None
    email = None
    phone = None
    skills = []
    experience = []
    education = []

    # Extract name (first PERSON entity)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
            break

    # Extract email and phone using regex
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    phone_pattern = r"\b\d{3}-\d{3}-\d{4}\b"
    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)
    email = email.group(0) if email else None
    phone = phone.group(0) if phone else None

    # Extract skills (customize based on common skills in job domain)
    skill_keywords = ["Python", "JavaScript", "SQL", "Java", "AWS", "Docker", "React"]
    for token in doc:
        if token.text in skill_keywords:
            skills.append(token.text)

    # Extract experience and education (basic heuristic)
    for sent in doc.sents:
        if "experience" in sent.text.lower():
            experience.append(sent.text)
        if "education" in sent.text.lower():
            education.append(sent.text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "experience": experience,
        "education": education
    }

if __name__ == "__main__":
    resume_data = parse_resume("resumes/sample_resume.pdf")
    print(resume_data) 