# Searching for "Corporate Governance" by Company
This repo contains scrapers for corporate governance searching of companies on Factiva and Nexis Uni, developed as a research project at Wilfrid Laurier University. These files are not and will not be maintained.  
_For an updated, robust Nexis Uni scraper please see my other repo [nexis-scraper](https://github.com/andrebodo/lexis-sentiment-indexer)._

The data service to filename mappings are as follows:

Nexis Uni: _nexis_scrape.py_  
Factiva: _factiva_scrape.py_  

Both of these scrapers are alpha code and have not been designed robustly. These scrapers should not be used to scrape large datasets. They were intended for use in preliminary scraping for data. Any scraping done using these files should be monitored closely, as error handling has not been implemented.

The Factiva file no longer does scraping. It currently functions as a login, and a (commented) attempt at solving captcha programmatically. 

The Nexis Uni scraper is unreliable by nature. This is largely due to the excessive and poor use of JS on the Nexis website, as well as slow querying. No attempts were made to increase robustness of this script. 

Several input csv files are required to make these scrapers work for this project:

Nexis Uni:  
search_largest_companies.csv: _list of companies which has 6 columns (Security ID, PERMNO, SDATE, EDATE, SCORE, COMPANY NAME - HISTORICAL)_  
search_sources.csv: _list of search source ID's (Nexis Uni URL API ID's) and human readable names for the publisher. This list can be constructed by consulting the Nexis Uni website to download their content listing. The columns are (ID, Publisher)_  
search_terms.csv: _single column list (Term) which contains search terms that will be joined by an 'or' clause._  

Factiva:  
There is no input file. The search string has been hardcoded into the script.

**Browser**  
Both scripts will look for chromedriver.exe in the same directory as the script. It is reccomended that you use chromedriver 85 or higher.

**Inputting your usercredentials:**  
factiva_scrape.py: _username and password and on lines 49 and 50 respectively_  
nexis_scrape.py: _username and password and on lines 77 and 78 respectively_  

**Specify download folder**  
You will need to specify a download folder for nexis scraper on line 58:  
example: _C:\\\\Users\\\\USERNAME\\\\nexis-scraper\\\\data\\\\_  

**What if I go to a different university?**  
You can change your library login url in each file on lines:  
factiva_scrape.py: _21_  
nexis_scrape.py: _57_  

The link is likely going to be found of your library's website. Copy the link which takes you to your login page. You may need to change the following lines to reflect differences in the browser html (which can be found by right-click -> inspect element):

factiva_scrape.py: _49 to 51_  
nexis_scrape.py: _77 to 79_  

**Terms & Conditions**  
Neither provider (Nexis Uni or Factiva) allow scraping. These scrapers have been developed for academic purposes. By using these scrapers you are responsible for all consequences of use. 

All files can be used and modified freely.

**A better scraper**  
To find a more robust and updated scraper developed for Nexis Uni only, please see my other repo at [nexis-scraper](https://github.com/andrebodo/lexis-sentiment-indexer)
