# What It Does
This website will scrape data from 2 different job search websites

# Sample 
![Alt text](https://user-images.githubusercontent.com/97370250/157504099-6ce49675-f7f9-421c-8c63-e35a6267c6e5.png)
![Alt text](https://user-images.githubusercontent.com/97370250/157504281-8b1253e9-4830-4d5b-bba8-254df8196a3c.png)

# Technologies 
Flask V 2.0.3, Python V 3.10, Beautiful Soup V Beautiful Soup 4

# Details
Given a job name/keyword, zip code, and the number of webpages you want to scrape per site, this website will return a table with jobs, specificly the website, the job name, the salary, and a snippet about the job. 
There are also filters in the website, You can filter by minimum salary, you can filter by company name, you can filter by age required, you can filter by hourly/yearly wages.
If you don't understand the website there is a help page with description of each tool.
*There are some functions in backend.py file which can make the data go to a SQL database instead of going to a list. 

# Status
The project is mostly finished, there might be a fix added if the website is updated, so it keeps webscraping correctly. 
