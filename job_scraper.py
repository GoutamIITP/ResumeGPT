import scrapy
from scrapy.crawler import CrawlerProcess

class JobSpider(scrapy.Spider):
    name = "job_spider"
    start_urls = ["https://www.indeed.com/jobs?q=software+engineer&l=Remote"]

    def parse(self, response):
        jobs = []
        for job in response.css("div.job_seen_beacon"):
            title = job.css("h2.jobTitle::text").get()
            company = job.css("span.companyName::text").get()
            location = job.css("div.companyLocation::text").get()
            description = job.css("div.job-snippet::text").get()
            link = job.css("a::attr(href)").get()
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "link": link
            })
        return jobs

def scrape_jobs():
    process = CrawlerProcess(settings={
        "FEEDS": {
            "jobs.json": {"format": "json"}
        },
        "USER_AGENT": "Mozilla/5.0",
        "ROBOTSTXT_OBEY": True
    })
    process.crawl(JobSpider)
    process.start()
    # Read the scraped jobs
    import json
    with open("jobs.json", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    jobs = scrape_jobs()
    print(jobs) 