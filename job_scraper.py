import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define the companies you want to scrape
companies = ["Tiber Health", "Ponce Health Sciences University", "Ponce Research Institute"]

# Base URL for Indeed job search
indeed_url = "https://www.indeed.com/jobs?q={}&start={}"

# Initialize an empty list to store job data
jobs = []

# Headers for the HTTP request to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
}

# Scrape Indeed
for company in companies:
    for page in range(0, 30, 10):  # Adjust page range as needed
        url = indeed_url.format(company.replace(" ", "+"), page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="jobsearch-SerpJobCard")

        for job in job_cards:
            job_title = job.find("h2", class_="title").text.strip()
            listed_company = job.find("span", class_="company").text.strip()
            location = job.find("div", class_="location").text if job.find("div", "location") else "N/A"
            summary = job.find("div", class_="summary").text.strip()
            job_url = "https://www.indeed.com" + job.find("a")["href"]

            if listed_company in companies:
                jobs.append({
                    "Title": job_title,
                    "Company": listed_company,
                    "Location": location,
                    "Summary": summary,
                    "URL": job_url
                })

        time.sleep(1)  # Pause to avoid rate-limiting

# Scrape TrinetHire
trinethire_url = "https://app.trinethire.com/companies/23018-tiber-health-public-benefit/jobs"
response = requests.get(trinethire_url)
soup = BeautifulSoup(response.text, "html.parser")
job_listings = soup.find_all("a", class_="job")

for job in job_listings:
    job_title = job.find("h2").text.strip()
    job_url = "https://app.trinethire.com" + job["href"]
    company = "Tiber Health"  # Hardcoded for TrinetHire jobs
    location = job.find("span", class_="job-location").text.strip() if job.find("span", "job-location") else "N/A"
    summary = job.find("div", class_="job-description").text.strip() if job.find("div", "job-description") else "N/A"

    jobs.append({
        "Title": job_title,
        "Company": company,
        "Location": location,
        "Summary": summary,
        "URL": job_url
    })

# Save jobs to JSON
df = pd.DataFrame(jobs)
df.to_json("jobs.json", orient="records")
print("Jobs saved to jobs.json")
