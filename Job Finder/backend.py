import requests
from bs4 import BeautifulSoup
import sqlite3 
import re

the_big_job_list = []

def reset_list():
    """
    removes alll jobs from the list
    """
    for job in the_big_job_list:
        the_big_job_list.remove(job)

def add_to_list(website, job_list):
    """
    given a job list, appends each value in job list, with the website to the_big_job_list
    """
    for job in job_list:
        mini_job_list = []
        mini_job_list.append(website)
        mini_job_list.append(job[0])
        mini_job_list.append(job[1])
        mini_job_list.append(job[2])
        the_big_job_list.append(mini_job_list)

def connect():
    """
    Adds the job_list table to db is it doesnt already exist
    """
    con = sqlite3.connect("jobs.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS job_list (id INTEGER PRIMARY KEY, website, job_name, salary, snippet)")
    con.commit()
    con.close()

def get_address(zip_code):
    """
    Takes in zip code, returns list with the first value being the city, the second value is state. ex ['austin', 'tx']
    """
    listo = []
    r = requests.get(f"https://www.getzips.com/cgi-bin/ziplook.exe?What=1&Zip={zip_code}&Submit=Look+It+Up")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("tr")
    place = all[-1]
    for row in place:
        listo.append(row.text)
    address = listo[2]
    address = address.lower()
    address = address.split(' ')
    if len(address) > 2:
        address = [address[0] + '' + address[1], address[2]]
    address[0] = address[0][0:-1]
    return address


def find_job_simplyhired(zip_code, job, page_num):
    """
    using the zip code and job given, it will scrape simplyhired for jobs. page_num is the amount of pages scraped, or it will go till no pages left
    """
    list_of_jobs = []
    location = get_address(zip_code)
    r = requests.get(f"https://www.simplyhired.com/search?q={job}&l={location[0]}%2C+{location[1]}")
    x = 0
    while x < int(page_num):
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        all_jobs = soup.findAll("div", {"class":"SerpJob-jobCard"})
        for job in all_jobs:
            new_job = []
            new_job.append(job.find("span", {"class":"JobPosting-labelWithIcon"}).text)
            if job.find("div", {"class":"jobposting-salary"}) is None:
                new_job.append("NA")
            else:
                new_job.append(job.find("div", {"class":"jobposting-salary"}).text) 
            new_job.append(job.find("p", {"class":"jobposting-snippet"}).text)
            new_job.append(job.find("span"))
            list_of_jobs.append(new_job)
        try:
            link = soup.find("a", {"class":"Pagination-link"})['href']
        except TypeError:
            return list_of_jobs
        r = requests.get(f"https://www.simplyhired.com{link}")
        if r is None:
            return list_of_jobs
        x = x + 1
    return list_of_jobs



def find_job_theladders(job,zipcode, pages):
    """
    using the zip code and job given, it will scrape simplyhired for jobs. page_num is the amount of pages scraped, or it will go till no pages left
    """
    tjob = job.split(' ')
    if len(tjob) > 1:
        Ljob = ""
        for word in tjob:
            Ljob = Ljob + word.lower() + "%20"
        r = requests.get(f"https://www.theladders.com/jobs/searchresults-jobs?keywords={Ljob[0:-3]}&location={zipcode}")
    
    job_list = []
    page = 0
    r = requests.get(f"https://www.theladders.com/jobs/searchresults-jobs?keywords={job}&location={zipcode}")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    max_page = int(re.sub("\D", "", soup.find("span", {"class":"job-title-header"}).text[0:-5]))
    max_page = max_page/25
    while page < int(pages):
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        all_jobs = soup.findAll("div", {"class":"job-card-container-with-labels"})
        if all_jobs is None:
            return job_list
        print(type(all_jobs))
        for job in all_jobs:
            print(type(job))
            cur_job = []
            cur_job.append(job.find("a", {"class":"job-card-title"}).text)
            if job.find("div", {"class":"job-card-salary-label"}) is None:
                cur_job.append("NA")
            else:
                cur_job.append(job.find("div", {"class":"job-card-salary-label"}).text)
            cur_job.append(job.find("p", {"class":"job-card-description"}).text)
            job_list.append(cur_job)
        page = page + 1
        if len(tjob) > 1:
            r = requests.get(f"https://www.theladders.com/jobs/searchresults-jobs?keywords={Ljob[0:-3]}&location={zipcode}")
        r = requests.get(f"https://www.theladders.com/jobs/searchresults-jobs?keywords={job}&location={zipcode}&page={page}")
    return job_list
    
def add_to_db(job_list, website):
    """
    Given a list job_list (the return value of find_job()), and a website, it will add it to the db
    """
    con = sqlite3.connect("jobs.db")
    cursor = con.cursor()
    for job in job_list:
        cursor.execute("INSERT INTO job_list VALUES (NULL, ?, ?, ?, ?)", (website, job[0], job[1], job[2]))
    con.commit()
    con.close()

def check_list():
    """
    checks that each list in the_big_job_list has exactly  values in it
    """
    for job in the_big_job_list:
        if len(job) != 4:
            the_big_job_list.remove(job)
    for job in the_big_job_list:
        if the_big_job_list.count(job) > 1:
            the_big_job_list.remove(job)

def find_age(age, db=False):
    """
    Given a age, it will return a list with jobs that require that age,  if db=True, does the action on the database instead of list
    """
    if db == True:
        con = sqlite3.connect("jobs.db")
        cursor = con.cursor()
        cursor.execute("SELECT snippet from job_list")
        snippets = cursor.fetchall()
        age_list = []
        for snippet in snippets:
            if f"{age} year" in  snippet[0]:
                age_list.append(snippet)
        for snippe in age_list:
            cursor.execute("SELECT website, job_name, salary, snippet FROM job_list WHERE snippet=?", (snippe))
        rok = cursor.fetchall()
        return rok
    if db == False:
        agee_list = []
        ageee_list = []
        snippets_list = []
        check_list()
        for job in the_big_job_list:
            snippets_list.append(job[3])
        for snipp in snippets_list:
            if f"{age} year" in snipp or f"age {age}" in snipp or f"{age} and" in snipp or f"{age} or" in snipp:
                agee_list.append(snipp)
        for p in agee_list:
            for jobb in the_big_job_list:
                if p == jobb[3]:
                    ageee_list.append(jobb)
        return ageee_list

def hourly_or_yearly(hourly=True, db=False):
    """
    If paramater is true, returns a list with hourly wages, if paramater is false, returns a list with yearly wages
    """
    if db == True:
        con = sqlite3.connect("jobs.db")
        cursor = con.cursor()
        cursor.execute("SELECT salary from job_list")
        salaries = cursor.fetchall()
        salary_list = []
        for salary in salaries:
            if hourly == True:
                if 'hour' in salary[0]:
                    salary_list.append(salary[0])
            else:
                if 'year' in salary[0]:
                    salary_list.append(salary[0])
        rok_list = []
        for salary in salary_list:
            cursor.execute("SELECT website, job_name, salary, snippet FROM job_list WHERE salary=?", (salary,))
            rok_list.append(cursor.fetchall())
        return rok_list
    else:
        salary_list2 = []
        check_list()
        for salary2 in the_big_job_list:
            if hourly == True:
                if 'hour' in salary2[2]:
                    salary_list2.append(salary2)
            else:
                if 'year' in salary2[2]:
                    salary_list2.append(salary2)
        return salary_list2

def get_reduced_salary(job_list):
    """
    given a job_list, it will reduce the salary to two numbers, like from [ ESTIMATE: $90,000k - $100,000k] to [90000, 100000]
    """
    salaries= []
    for job in job_list:
        salaries.append(job[2])

    for item in range(len(salaries)):
        cur_str = salaries[item]
        cur_str = cur_str.split(' ')
        salaries[item] = cur_str

    for job_salary in salaries:
        for counter in range(len(job_salary)):
           job_salary[counter] = re.sub("\D", "", job_salary[counter])
        for item in job_salary:
            if item == '':
               job_salary.remove(item)
               counter = counter - 1
            counter = counter + 1

    return salaries

def find_salary(salary, hourly=True):
    """
    Given a minimum salary, and houly or yearly salary, it will return all jobs with the salary requirments
    """
    salaries = []
    if hourly == True:
        hour_list = get_reduced_salary(hourly_or_yearly())
        for pair in hour_list:
            for number in range(len(pair)):
                if pair[number] != '':
                    if int(pair[number]) >= 1000:
                        pair[number] = int(pair[number])/100

        for pair2 in range(len(hour_list)):
            if salary <= int(hour_list[pair2][0]):
                salaries.append(hourly_or_yearly()[pair2])
        return salaries
    else:
        year_list = get_reduced_salary(hourly_or_yearly(False))
        for pair in year_list:
            for number in range(len(pair)):
                if pair[number] != '':
                    if int(pair[number]) < 1000:
                        pair[number] = int(pair[number]) * 1000

        for pair2 in range(len(year_list)):
            if salary <= int(year_list[pair2][0]):
                salaries.append(hourly_or_yearly(False)[pair2])
        return salaries

def get_by_company(company_name):
    all_companies = []
    for company in the_big_job_list:
        if company_name.lower() in company[1].lower():
            all_companies.append(company)
    return all_companies
