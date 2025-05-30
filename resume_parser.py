import pdfplumber
import re
from transformers import pipeline

# Load pre-trained NER model
nlp = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

def parse_resume(file_path):
    # Extract text from PDF
    try:
        with pdfplumber.open(file_path) as pdf:
            text = "".join(page.extract_text() for page in pdf.pages if page.extract_text())
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

    # Initialize extracted data
    extracted_data = {
        "name": "Not found",
        "email": "Not found",
        "phone": "Not found",
        "skills": [],
        "experience": [],
        "education": []
    }

    # Extract name using NER
    ner_results = nlp(text)
    name_parts = []
    for entity in ner_results:
        if entity["entity_group"] == "PER":
            name_parts.append(entity["word"])
    if name_parts:
        extracted_data["name"] = " ".join(name_parts).replace("##", "").strip()

    # Extract email with regex
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    email_match = re.search(email_pattern, text, re.IGNORECASE)
    if email_match:
        extracted_data["email"] = email_match.group(0)

    # Extract phone with regex (handles multiple formats)
    phone_patterns = [
        r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",  # 123-456-7890, 123.456.7890, 123 456 7890
        r"\b\d{10}\b",                          # 1234567890
        r"\+\d{1,3}\s?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"  # +1 123-456-7890
    ]
    for pattern in phone_patterns:
        phone_match = re.search(pattern, text)
        if phone_match:
            extracted_data["phone"] = phone_match.group(0)
            break

    # Extract skills, experience, and education using section detection
    lines = text.split("\n")
    current_section = None
    skill_keywords = [
        "Python", "JavaScript", "SQL", "Java", "AWS", "Docker", "React", 
        "Node.js", "C++", "HTML", "CSS", "Leadership", "Project Management"
    ]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect section headers
        if any(keyword in line.lower() for keyword in ["skills", "technical skills", "proficiencies"]):
            current_section = "skills"
            continue
        elif any(keyword in line.lower() for keyword in ["experience", "work experience", "professional experience"]):
            current_section = "experience"
            continue
        elif any(keyword in line.lower() for keyword in ["education", "academic background", "qualifications"]):
            current_section = "education"
            continue

        # Extract content based on current section
        if current_section == "skills":
            # Split line by commas or semicolons for skills
            potential_skills = [s.strip() for s in re.split(r"[;,]", line)]
            for skill in potential_skills:
                if any(keyword.lower() in skill.lower() for keyword in skill_keywords):
                    if skill not in extracted_data["skills"]:
                        extracted_data["skills"].append(skill)
        elif current_section == "experience":
            if line not in extracted_data["experience"]:
                extracted_data["experience"].append(line)
        elif current_section == "education":
            if line not in extracted_data["education"]:
                extracted_data["education"].append(line)

    # Fallback for skills if no section is found
    if not extracted_data["skills"]:
        for word in text.split():
            if word in skill_keywords and word not in extracted_data["skills"]:
                extracted_data["skills"].append(word)

    # Clean up empty or placeholder lists
    for key in ["skills", "experience", "education"]:
        if not extracted_data[key]:
            extracted_data[key] = ["None identified"]

    return extracted_data

if __name__ == "__main__":
    sample_file = "resumes/sample_resume.pdf"  # Replace with actual path
    data = parse_resume(sample_file)
    if data:
        import json
        print(json.dumps(data, indent=4)) 