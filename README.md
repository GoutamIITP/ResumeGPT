# ResumeGPT Resume Parser

This project implements a web application using Flask and Generative AI to parse resumes (PDF/Word) and extract structured data.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Usage](#usage)
- [Ethical Guidelines and Data Privacy](#ethical-guidelines-and-data-privacy)
- [Future Improvements](#future-improvements)

## Features

- Upload PDF and Word (.docx) resumes.
- Use Generative AI (Hugging Face Transformers) for resume parsing and entity extraction (Name, Email, Phone, Skills, Experience, Education).
- Display extracted data in a user-friendly web interface.
- Basic data privacy measures (temporary storage, file deletion).

## Tech Stack

- **Backend:** Python, Flask, pdfplumber, transformers, torch.
- **Frontend:** HTML, Tailwind CSS.
- **Storage:** Temporary file storage.

## Setup

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd resumegpt
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv resumegpt_env
   source resumegpt_env/bin/activate  # On Windows: resumegpt_env\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *(Note: You might need to install additional libraries like `python-docx` if not already in `requirements.txt` for Word support, and potentially download a spaCy model if using spaCy for NER.)*

## Usage

1. **Run the Flask application:**

   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to `http://localhost:5000`.

3. **Upload a PDF or Word resume** using the form.

4. **View the extracted structured data** on the results page.

## Ethical Guidelines and Data Privacy

- Uploaded resumes are intended for temporary processing only and are deleted after parsing.
- We aim to comply with data privacy regulations like GDPR/CCPA.
- **Important:** The current implementation uses basic file handling. For production environments, enhance security with proper encryption and secure storage solutions.
- User consent for data processing is a critical consideration for production deployments.

## Future Improvements

- Integrate with a more advanced Gen AI model (e.g., xAI Grok 3 API) for improved parsing accuracy.
- Implement robust encryption for uploaded files.
- Add user authentication and management.
- Enhance the frontend with more detailed and interactive display of extracted data.
- Implement more sophisticated entity extraction and data structuring logic.
- Add support for other resume formats.
- Incorporate job scraping and application management features as outlined in the initial project description.

Dependencies

* Flask

* PyPDF2

* pdfplumber

* transformers

* torch

* requests

* BeautifulSoup

* Selenium

* Pandas

* reportlab 