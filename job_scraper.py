import requests
from bs4 import BeautifulSoup
import csv

URL = "https://realpython.github.io/fake-jobs/"

def scrape_jobs():
    response = requests.get(URL)

    if response.status_code != 200:
        print("❌ Failed to fetch the website")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    job_cards = soup.find_all("div", class_="card-content")

    jobs_data = []

    for job in job_cards:
        title = job.find("h2", class_="title")
        company = job.find("h3", class_="company")
        location = job.find("p", class_="location")
        link_tag = job.find("a", string="Apply")

        job_title = title.text.strip() if title else "N/A"
        company_name = company.text.strip() if company else "N/A"
        job_location = location.text.strip() if location else "N/A"

        job_url = "N/A"
        if link_tag and link_tag.get("href"):
            job_url = URL + link_tag.get("href")

        jobs_data.append({
            "Job Title": job_title,
            "Company Name": company_name,
            "Location": job_location,
            "Job URL": job_url
        })

    return jobs_data


def save_to_csv(data):
    with open("fake_jobs.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Job Title", "Company Name", "Location", "Job URL"])

        for job in data:
            writer.writerow([job["Job Title"], job["Company Name"], job["Location"], job["Job URL"]])

    print("✅ All job data saved into fake_jobs.csv successfully!")


if __name__ == "__main__":
    jobs = scrape_jobs()
    print(f"📌 Total Jobs Scraped: {len(jobs)}")

    save_to_csv(jobs)
