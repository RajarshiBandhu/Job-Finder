from httpcore import request
from flask import Flask, url_for, render_template, request
from backend import *
import requests

app = Flask(__name__)

@app.route("/")
def home():
    reset_list()
    return render_template("index.html", all_data = the_big_job_list)

@app.route("/search-job/")
def search_job():
    reset_list()
    job = request.args.get("job")
    zipcode = request.args.get("zipcode")
    pages = request.args.get("pages")
    add_to_list("www.simplyhired.com", find_job_simplyhired(zipcode, job, pages))
    add_to_list("www.theladders.com", find_job_theladders(job, zipcode, pages))
    check_list()
    return render_template("jobs.html", all_data = the_big_job_list)

@app.route("/filter-company/")
def searchcompany():
    company=request.args.get("company")
    return render_template("jobs.html", all_data=get_by_company(company))
    
@app.route("/hourly-wages/")
def hourly_wage():
    return render_template("jobs.html", all_data=hourly_or_yearly())
    
@app.route("/yearly-wages/")
def yearly():
    return render_template("jobs.html", all_data=hourly_or_yearly(hourly=False))

@app.route("/all-jobs/")
def all_jobs():
    return render_template("jobs.html", all_data=the_big_job_list)

@app.route("/find-age/")
def findbyage():
    age = request.args.get("age")
    return render_template("jobs.html", all_data=find_age(age))

@app.route("/filter-salary-hour/")
def findsalaryhour():
    salary = int(request.args.get("salary"))
    return render_template("jobs.html", all_data = find_salary(salary, True))

@app.route("/filter-salary-year/")
def findsalaryyear():
    salary = int(request.args.get("salary"))
    return render_template("jobs.html", all_data=find_salary(salary, False))

if __name__=="__main__":
    app.run()
    
