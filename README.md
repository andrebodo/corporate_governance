# corporate_governance
This repo contains scrapers used for corporate governance searching on Factiva and Nexis Uni, developed for a research project at Wilfrid Laurier University

The data service to filename mappings are as follows:
Nexis Uni: nexis_scrape.py
Factiva: factiva_scrape.py

Both of these scrapers are alpha code and have not been designed robustly. These scrapers should not be used to scrape large datasets. They were intended for use in preliminary scraping for data. Any scraping done using these files should be monitored closely, as error handling has not been implemented.

The Factiva scraper does not overcome the issues with captcha. Several attempts were made to overcome the captcha limitations, however no feasbile solution was found. 

The Nexis Uni scraper is unreliable by nature. This is largely due to the excessive and poor use of JS on the Nexis website, as well as slow querying. No attempts were made to increase robustness of this script. 
