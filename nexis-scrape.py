import os
import re
import time
import pandas as pd

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1200)


def custom_click(driver_handle, button):
    try:
        driver_handle.execute_script('arguments[0].click();', button)
        return True
    except StaleElementReferenceException:
        return False

# Function to dealt with stupid javascript buttons
def custom_load_wait_click(driver, comparator_xpath, button, timeout=60):
    source = driver.find_element_by_xpath(comparator_xpath).get_attribute('innerHTML')
    driver.execute_script("arguments[0].click();", button)
    def compare_source(driver):
        try:
            return source != driver.find_element_by_xpath(comparator_xpath).get_attribute('innerHTML')
        except WebDriverException as wde:
            print(wde)
            pass
    WebDriverWait(driver, timeout).until(compare_source)


def build_urls():
    search_term = ' or '.join([s.replace('"', '%22') for s in pd.read_csv('search_terms.csv')['Term']])
    search_source = '&source='.join([s for s in pd.read_csv('search_sources.csv')['ID']])

    url_base = 'http://advance.lexis.com.libproxy.wlu.ca/api'
    company_df = pd.read_csv('search_largest_companies.csv', parse_dates=['SDATE', 'EDATE'],
                             usecols=list(range(6)), dtype={'Security ID': str})
    company_df.columns = ['secID', 'permno', 'sdate', 'edate', 'score', 'companyName']
    company_df['sdate'] = company_df['sdate'].apply(datetime.strftime, args=('%Y',))
    company_df['edate'] = company_df['edate'].apply(datetime.strftime, args=('%Y',))
    company_df['url'] = f'{url_base}/search?q={search_term} and company(' + company_df["companyName"] \
                        + ')&collection=news&qlang=bool' \
                        + '&startdate=' + company_df['sdate'] + '&enddate=' + company_df['edate'] \
                        + f'&source={search_source}&context=1516831'
    company_df['url'] = company_df['url'].str.replace(' ', '%20')

    return company_df


if __name__ == '__main__':
    login_url = 'https://libproxy.wlu.ca/login?auth=shibboleth&url=http://www.nexisuni.com'
    download_path = 'C:\\Users\\Andre\\Documents\\_Python Projects\\nexis-scraper\\data\\'

    prefs = {
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'download.default_directory': download_path
    }

    chrome_exe_path = 'chromedriver.exe'

    # Selenium
    chrome_opts = webdriver.ChromeOptions()
    chrome_opts.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=chrome_exe_path, options=chrome_opts)
    wait = WebDriverWait(driver, 15, poll_frequency=1)

    # Login
    driver.get(login_url)
    base_window = driver.current_window_handle
    driver.find_element_by_id('username').send_keys('')
    driver.find_element_by_id('password').send_keys('')
    driver.find_element_by_xpath('//*[@class="form-submit"]').click()

    df = build_urls()  # Get URLS for company searches
    download_timeout = 60 * 5

    RE_INT = re.compile(r'\([0-9]+\)')  # regexp for determining if there are any results found
    df_notfound = pd.DataFrame(columns=df.columns)

    # Test 100 URLS
    for i in range(len(df)):
        url = df.loc[i, 'url']
        driver.get(url)

        # See if there are any results, if not continue
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='resultsHeader']")))
        e = driver.find_element_by_xpath("//*[@class='resultsHeader']")
        result_count_str = e.find_element_by_tag_name('span').text
        if int(re.findall('[0-9]+', result_count_str)[0]) == 0:
            df_notfound = df_notfound.append(df.iloc[i, :], ignore_index=True)
            continue

        # Results organization
        e = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@data-action='viewmin']")))
        driver.execute_script("arguments[0].click();", e)
        e = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@data-action='toggleduplicates']")))
        driver.execute_script("arguments[0].click();", e)
        e = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-action='sortby']")))
        driver.execute_script("arguments[0].click();", e)
        e = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-value='dateascending']")))
        driver.execute_script("arguments[0].click();", e)
        time.sleep(10)

        # Page count
        e = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='pagination']/ol/li")))
        page_count = int(e[-2].text)
        file_count = 0
        url_history = []

        reload_checkpoint = False

        # Scraping
        page = 1
        while True:

            if reload_checkpoint:
                print(f'reloading from last checkpoint: {url_history[-1]}')  # load checkpoint
                driver.get(url_history[-1])
                # go forward one page
                e = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-action='nextpage']")))
                custom_click(driver, "//ol[@class='nexisuni-result-list']", e)
                # update page and file count
                e = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='current']/span")))
                page = int(e.text)
                file_count = len(url_history) + 1
                reload_checkpoint = False

            file_name = f"{i}_{df.loc[i, 'secID']}_batch{file_count}"

            # select all records
            e = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='results-list-delivery-toolbar']/div/ul[1]/li[1]/input")))
            driver.execute_script("arguments[0].click();", e)
            time.sleep(1)

            # download page
            if page % 10 == 0 or page == page_count:
                if f'{file_name}.zip' not in [x.lower() for x in os.listdir(download_path)]:
                    e = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-action='downloadopt']")))
                    driver.execute_script("arguments[0].click();", e)

                    # basic options
                    e = WebDriverWait(driver, 60, poll_frequency=1).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@id='FileName']")))
                    e.clear()
                    e.send_keys(file_name)
                    e = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='Rtf']")))
                    if e.get_attribute('checked') != 'true': e.click()
                    e = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='SeparateFiles']")))
                    if e.get_attribute('checked') != 'true': e.click()
                    # format options
                    e = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='tab-FormattingOptions']")))
                    driver.execute_script("arguments[0].click();", e)
                    e = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='IncludeCoverPage']")))
                    if e.get_attribute('checked'): driver.execute_script("arguments[0].click();", e)
                    e = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@id='DisplayFirstLastNameEnabled']")))
                    if e.get_attribute('checked'): driver.execute_script("arguments[0].click();", e)
                    e = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='PageNumberSelected']")))
                    if e.get_attribute('checked'): driver.execute_script("arguments[0].click();", e)
                    e = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='EmbeddedReferences']")))
                    if e.get_attribute('checked'): driver.execute_script("arguments[0].click();", e)
                    e = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@id='SearchTermsInBoldTypeEnabled']")))
                    if e.get_attribute('checked'): driver.execute_script("arguments[0].click();", e)
                    e = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@id='SearchTermsInItalicTypeEnabled']")))
                    if e.get_attribute('checked'): driver.execute_script("arguments[0].click();", e)
                    e = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@id='SearchTermsUnderlinedEnabled']")))
                    if e.get_attribute('checked'): driver.execute_script("arguments[0].click();", e)
                    e = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@id='DisplayPaginationInBoldEnabled']")))
                    if e.get_attribute('checked'): driver.execute_script("arguments[0].click();", e)

                    # download
                    e = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-action='download']")))
                    driver.execute_script("arguments[0].click();", e)

                    start_time = time.time()
                    while True:
                        if time.time() - start_time > download_timeout:
                            reload_checkpoint = True  # Reload from last checkpoint if download failed
                            break
                        if f'{file_name}.zip' in [x.lower() for x in os.listdir(download_path)]:
                            now = datetime.now().strftime('%H:%M:%S')
                            print(f'{now} download completed: {file_name}.zip')
                            file_count += 1
                            url_history.append(driver.current_url)
                            break
                        time.sleep(5)  # wait before checking again.
                else:
                    file_count += 1
                    # deselect all records if file exists
                    e = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="results-list-delivery-toolbar"]/div/ul[1]/li[2]/div/button/span[2]')))
                    driver.execute_script("arguments[0].click();", e)
                    e = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="viewtray-dropdown"]/div/div[1]/div/button')))
                    driver.execute_script("arguments[0].click();", e)
                    e = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/aside/footer/div/button[1]')))
                    driver.execute_script("arguments[0].click();", e)
                    time.sleep(1)

            # navigate to next page
            if page < page_count:
                e = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-action='nextpage']")))
                custom_load_wait_click(driver, "//ol[@class='nexisuni-result-list']", e)
                page += 1
            else:
                now = datetime.now().strftime('%H:%M:%S')
                print(f'{now} {df.loc[i, "secID"]} completed')
                break

    df_notfound.to_csv('no_results_method_2.csv')
