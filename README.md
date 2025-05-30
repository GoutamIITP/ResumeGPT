# ResumeGPT: AI-Powered Resume Parser

ResumeGPT is a web application designed to parse resumes (PDF and Word formats) using Generative AI and extract key information such as contact details, skills, experience, and education. The extracted structured data is then displayed on a user-friendly frontend interface.

This project focuses on the core resume parsing and data extraction functionality, laying the groundwork for more advanced features like job matching and automated applications.

## Features

-   **Resume Upload:** Supports uploading resumes in PDF (.pdf) and Word (.docx) formats via a simple web form.
-   **AI-Powered Parsing:** Utilizes a Hugging Face Transformers model (`dslim/bert-base-NER`) combined with regex and heuristic section detection to extract structured data (Name, Email, Phone, Skills, Experience, Education).
-   **Structured Data Display:** Presents the extracted information in a clean, organized, and responsive format on a dedicated results page.
-   **User Consent:** Includes a mandatory consent checkbox for data processing, emphasizing user privacy.
-   **Real-time UI Feedback:** Provides visual feedback during file upload and processing using JavaScript and a loading spinner.
-   **Temporary Storage:** Uploaded resumes are stored temporarily and automatically deleted after parsing to enhance privacy.

## Technology Stack

-   **Backend:**
    -   Python
    -   Flask: Web framework for handling requests and rendering templates.
    -   `pdfplumber`: For extracting text from PDF files.
    -   `python-docx`: For extracting text from Word (.docx) files.
    -   `transformers`: Leveraging Hugging Face models for Named Entity Recognition (NER).
    -   `torch`: Deep learning framework dependency for `transformers`.
-   **Frontend:**
    -   HTML5: Structure of the web pages.
    -   Tailwind CSS: Utility-first CSS framework for rapid styling and responsiveness.
    -   JavaScript: For frontend interactivity, file validation, and loading states.
-   **Other Libraries (Used in project plan but potentially for future features):** `requests`, `beautifulsoup4`, `Selenium`, `Pandas`, `reportlab`, `spacy`, `scrapy`, `gunicorn` (for deployment), `cryptography` (for optional encryption).

## Prerequisites

Before you begin, ensure you have met the following requirements:

*   Python 3.8+
*   `pip` (Python package installer)
*   A stable internet connection to download models and dependencies.

## Setup

Follow these steps to set up and run the project locally:

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd resumegpt
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv .venv
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows:
    .\.venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Flask application:**

    ```bash
    python app.py
    ```

    The application will start, and you should see output indicating the development server is running.

2.  **Open your web browser** and navigate to `http://127.0.0.1:5000/`.

3.  **Upload a Resume:**
    *   On the upload page, select a PDF or Word (.docx) resume file.
    *   Check the consent box to agree to data processing.
    *   Click the "Upload and Parse" button.

4.  **View Extracted Data:**
    *   The application will process the resume (a loading spinner will be shown).
    *   You will be redirected to the results page displaying the extracted Name, Email, Phone, Skills, Experience, and Education sections.

5.  **Upload Another:** Click the "Upload Another Resume" button to return to the upload page.

## Ethical Considerations and Data Privacy

-   **Temporary Processing:** Uploaded resumes are processed in memory and/or stored temporarily only as needed for parsing. They are deleted from the server's temporary storage immediately after processing is complete.
-   **User Consent:** Explicit consent is required from the user before processing their resume data.
-   **Transparency:** The application clearly states the purpose of data processing and the temporary nature of storage.
-   **Disclaimer:** This is a demonstration project. For production deployments handling sensitive user data, significantly more robust security measures (e.g., strong encryption at rest and in transit, secure storage solutions, detailed privacy policy) are essential to comply with regulations like GDPR, CCPA, etc.

## Project Structure

```
resumegpt/
├── app.py                  # Main Flask application
├── resume_parser.py        # Resume parsing logic
├── templates/             # HTML templates
│   ├── index.html        # Resume upload form
│   └── results.html      # Display extracted data
├── static/                # Static files (CSS, JS)
│   ├── script.js         # Frontend JavaScript
│   └── style.css         # Custom CSS
├── resumes/               # Temporary storage for uploaded resumes (created by app.py)
├── README.md             # Project documentation
└── requirements.txt       # Python dependencies
```

## Future Enhancements

Based on the initial project vision, the following features could be added:

-   **Improved Parsing:** Integrate more advanced Gen AI models (e.g., fine-tuned models or commercial APIs like xAI Grok 3, if available) for higher accuracy in entity and section extraction.
-   **Robust Data Extraction:** Enhance parsing logic to better handle complex resume formats, tables, and less common section titles.
-   **Advanced Security:** Implement robust encryption for resumes temporarily stored on the server.
-   **Error Handling & Feedback:** More detailed error messages and user guidance for parsing failures.
-   **Job Matching:** Develop functionality to match extracted resume skills and experience with job descriptions.
-   **Automated Applications:** Implement features for tailoring resumes/cover letters and submitting applications to job boards.
-   **User Management:** Add authentication and user profiles.
-   **Frontend Improvements:** More interactive display of data, options to edit extracted information, downloadable results.

## Contributing

Contributions are welcome! Please follow standard practices: Fork the repository, create a branch, and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE). (Note: Create a LICENSE file if you don't have one.) 