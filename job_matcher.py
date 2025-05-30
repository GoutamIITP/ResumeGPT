import scrapy
from scrapy.crawler import CrawlerProcess
from transformers import pipeline
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

# Initialize embedding pipeline
embedder = pipeline("feature-extraction", model="distilbert-base-uncased")

class JobSpider(scrapy.Spider):
    name = "job_spider"
    start_urls = ["https://www.indeed.com/jobs?q=software+engineer&l=Remote"]

    def parse(self, response):
        jobs = []
        # Adjust selectors based on actual job board structure if needed
        for job in response.css("div.job_seen_beacon"):
            title = job.css("h2.jobTitle::text").get()
            company = job.css("span.companyName::text").get()
            location = job.css("div.companyLocation::text").get()
            description = job.css("div.job-snippet::text").get()
            link = job.css("a::attr(href)").get()
            if title and company and location and description and link:
                 jobs.append({
                "title": title.strip() if title else None,
                "company": company.strip() if company else None,
                "location": location.strip() if location else None,
                "description": description.strip() if description else None,
                "link": link.strip() if link else None
            })
        return jobs

def get_text_embedding(text):
    # Ensure text is not None or empty
    if not text:
        return np.zeros(embedder.model.config.dim)
    # Handle potential truncation or batching if necessary for long texts
    embeddings = embedder(text, return_tensors="pt", truncation=True)[0].numpy().mean(axis=0)
    return embeddings

def match_jobs(resume_data, jobs):
    if not resume_data or not jobs:
        return []
        
    # Combine relevant resume data for embedding
    resume_parts = [
        resume_data.get("name", ""),
        resume_data.get("email", ""),
        resume_data.get("phone", ""),
        " ".join(resume_data.get("skills", [])),
        " ".join(resume_data.get("experience", [])),
        " ".join(resume_data.get("education", []))
    ]
    resume_text = " ".join(filter(None, resume_parts))
    
    if not resume_text:
        return [] # Cannot match jobs without resume content

    try:
        resume_embedding = get_text_embedding(resume_text)
    except Exception as e:
        print(f"Error generating resume embedding: {e}")
        return []

    matched_jobs = []
    for job in jobs:
        job_description = job.get("description")
        if not job_description:
            continue # Skip jobs with no description

        try:
            job_embedding = get_text_embedding(job_description)
            similarity = cosine_similarity(resume_embedding.reshape(1, -1), job_embedding.reshape(1, -1))[0][0]
            if similarity > 0.7:  # Adjustable threshold
                matched_jobs.append({**job, "similarity": float(similarity)})
        except Exception as e:
            print(f"Error processing job {job.get('title', 'Unknown')}: {e}")
            continue
    
    return sorted(matched_jobs, key=lambda x: x["similarity"], reverse=True)

def scrape_jobs():
    # Ensure the output directory for scraped jobs exists
    output_file = "jobs.json"
    # Create a dummy jobs.json file for now since live scraping can be complex
    # In a real application, you would configure and run the Scrapy crawler
    dummy_jobs = [
        {"title": "Software Engineer", "company": "Tech Solutions", "location": "Remote", "description": "Looking for a Python developer with experience in Flask and AI.", "link": "http://example.com/job1"},
        {"title": "Data Scientist", "company": "Data Insights", "location": "New York", "description": "Seeking a data scientist skilled in Python, Pandas, and machine learning.", "link": "http://example.com/job2"},
        {"title": "Frontend Developer", "company": "Web Innovators", "location": "San Francisco", "description": "Need a React developer for building modern user interfaces.", "link": "http://example.com/job3"}
    ]
    
    try:
        with open(output_file, "w") as f:
            json.dump(dummy_jobs, f, indent=4)
        print(f"Created dummy {output_file} for testing.")
        return dummy_jobs # Return dummy data for now
    except Exception as e:
        print(f"Error creating dummy jobs.json: {e}")
        return []

if __name__ == "__main__":
    # This part is for testing the job matching logic
    resume_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "123-456-7890",
        "skills": ["Python", "Flask", "AI"],
        "experience": ["Developed a web application using Flask and integrated an AI model."],
        "education": ["BS Computer Science"]
    }
    
    print("Scraping jobs (using dummy data for now)...")
    jobs = scrape_jobs()
    print(f"Found {len(jobs)} jobs.")

    print("Matching jobs...")
    matched_jobs = match_jobs(resume_data, jobs)
    print("Matched Jobs:")
    for job in matched_jobs:
        print(f"- {job['title']} at {job['company']} (Similarity: {job['similarity']:.2f})") 