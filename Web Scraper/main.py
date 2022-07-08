from bs4 import BeautifulSoup
import requests
import time

# Allows user to input skill they are not familiar with
print('Put unfamiliar skill here')
unfamiliar_skill = input('>')
print('Filtering out', unfamiliar_skill)


def find_jobs():
    # Gets URL of page for scraping
    html_text = requests.get(
        'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    # Takes html of page and converts to lxml string
    soup = BeautifulSoup(html_text, 'lxml')
    # Looks for job(s) with <li> tag and className of clearfix job-bx wht-shd-bx (can use find_all to search all postings)
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    # Iterates through job list and job content
    for index, job in enumerate(jobs):
        # Returns published date by digging into span, then digging into the inner span and returning only text
        published_date = job.find('span', class_="sim-posted").span.text
        # Checks to see if Posted is included in the published date <span>
        if 'Posted' in published_date:
            # Varialbe which returns all company name in a job posting
            company_name = job.find(
                'h3', class_='joblist-comp-name').text.replace(' ', '')
        # Varialbe which returns all key skills in a job posting
            skills = job.find(
                'span', class_='srp-skills').text.replace(' ', '')
        # Varialbe which returns all job posting links in a job posting
            more_info = job.header.h2.a['href']
        # Checks list of skills in each posting for unfamiliar_skill and filters out info returned based on that
            if unfamiliar_skill not in skills:
                # Puts each job post from a search (every 10 minutes) into a txt file named 1.txt, 2.txt, 3.txt...
                with open(f'posts/{index}.txt', 'w') as f:
                    f.write(f"Company Name:  {company_name}\n")
                    f.write(f"Required Skills: {skills}\n")
                    f.write(f"Post URL: {more_info}")
                print(f'File saved: {index}')

# Runs the function to fetch job postings every 10 minutes
if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
