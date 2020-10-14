# corporate_governance
This repo contains scrapers for corporate governance searching of companies on Factiva and Nexis Uni, developed as a research project at Wilfrid Laurier University

The data service to filename mappings are as follows:

_Nexis Uni: nexis_scrape.py_  
_Factiva: factiva_scrape.py_  

Both of these scrapers are alpha code and have not been designed robustly. These scrapers should not be used to scrape large datasets. They were intended for use in preliminary scraping for data. Any scraping done using these files should be monitored closely, as error handling has not been implemented.

The Factiva scraper does not overcome the issues with captcha. Several attempts were made to overcome the captcha limitations, however no feasbile solution was found. 

The Nexis Uni scraper is unreliable by nature. This is largely due to the excessive and poor use of JS on the Nexis website, as well as slow querying. No attempts were made to increase robustness of this script. 

Several input csv files are required to make these scrapers work for this project:

Nexis Uni:

_search_largest_companies.csv: list of companies which has 6 columns (Security ID, PERMNO, SDATE, EDATE, SCORE, COMPANY NAME - HISTORICAL)_  
_search_sources.csv is a list of search source ID's (Nexis Uni URL API ID's) and human readable names for the publisher. This list can be constructed by consulting the Nexis Uni website to download their content listing. The columns are (ID, Publisher)_  
_search_terms.csv is a single column list (Term) which contains search terms that will be joined by an 'or' clause._  

Factiva:

There is no input file. The search string has been hardcoded into the script.

Guide to inputting your usercredentials:

_factiva_scrape.py: username and password and on lines () respectively_  
_nexis_scrape.py: username and password and on lines () respectively_  

**What if go to a different university?**

You can change your library login url in each file on lines:

_factiva_scrape.py:_  
_nexis_scrape.py:_  

The link is likely going to be found of your library's website. Copy the link which takes you to your login page. You may need to change the following lines to reflect differences in the browser html (which can be found by right-click -> inspect element):

_factiva_scrape.py: to _  
_nexis_scrape.py: to _  

**Terms & Conditions**

Neither provider (Nexis Uni or Factiva) allow scraping. These scrapers have been developed for academic purposes. By using these scrapers you are responsible for all consequences of use. 

All files can be used and modified freely.
