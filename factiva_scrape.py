import os
import time
import math
import random

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_between(a, b):
    rand = random.uniform(a, b)
    time.sleep(rand)


if __name__ == '__main__':
    cwd = Path.cwd()
    login_url = 'https://libproxy.wlu.ca/login?url=https://global.factiva.com/en/sess/login.asp?xsid=S003sbiZdJfZGn73XmnOHmnMDanMDQmMpUr5DByMU38ODJ9RcyqUUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUEA'
    download_path = str(cwd) + '\\data\\'
    download_timeout = 60 * 2

    prefs = {
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'download.default_directory': download_path
    }

    chrome_exe_path = str(cwd) + r'\chromedriver.exe'

    # Selenium
    chrome_opts = webdriver.ChromeOptions()
    chrome_opts.add_argument("start-maximized")
    chrome_opts.add_experimental_option('prefs', prefs)
    chrome_opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_opts.add_experimental_option('useAutomationExtension', False)
    # chrome_opts.add_argument('--disable-gpu')
    # chrome_opts.add_argument("--disable-blink-features")  # Prevent captcha
    # chrome_opts.add_argument("--disable-blink-features=AutomationControlled")  # Prevent captcha
    driver = webdriver.Chrome(executable_path=chrome_exe_path, options=chrome_opts)
    wait = WebDriverWait(driver, 15, poll_frequency=1)

    # Login
    driver.get(login_url)
    time.sleep(1)
    base_window = driver.current_window_handle
    driver.find_element_by_id('username').send_keys('***********************')
    driver.find_element_by_id('password').send_keys('***********************')
    driver.find_element_by_xpath('//*[@class="form-submit"]').click()

    time.sleep(30)

    # Search
    search_url = 'https://global-factiva-com.libproxy.wlu.ca/en/du/headlines.asp?napc=S&searchText=crude+oil+or+opec*+or+brent+or+wti+or+interstate+oil+compact+commission+or+iogcc+or+interstate+oil+and+gas+compact+comission+or+hydraulic+fracturing+or+hydrofracking+or+fracking+or+fracing+or+hydrofracturing+or+oil+sands+or+bitumen+or+crude+bitumen+or+tar+sands+or+oil+futures+or+wti+futures+or+wti+crude+futures+or+wti+crude+oil+futures+or+brent+futures+or+brent+crude+futures+or+brent+crude+oil+futures+or+non-opec*+or+oil+and+trade+or+strategic+petroleum+reserve+or+sweet+crude+or+sour+crude+or+light+crude+or+petroleum+supply+monthly+or+petroleum+monthly+supply+or+short-term+energy+outlook+or+petroleum&exclude=Obituaries|Recurring|Republished&dateRangeMenu=custom&dateFormat=iso&dateFrom=20050101&dateTo=20151231&sortBy=y&currentSources=U%7cglob%2cj%2cwp%2cfinp%2cnytf%2cec&currentSourcesDesc=sc_u_glob%2cThe+Globe+and+Mail+(Canada)%3bsc_u_j%2cThe+Wall+Street+Journal%3bsc_u_wp%2cThe+Washington+Post%3bsc_u_finp%2cNational+Post+(Canada)%3bsc_u_nytf%2cThe+New+York+Times%3bsc_u_ec%2cThe+Economist+(United+Kingdom)&searchLanguage=custom&searchLang=EN&dedupe=1&srchuiver=2&accountid=9WIL002400&namespace=18'
    driver.get(search_url)

    # Page Count
    e = driver.find_element_by_class_name('resultsBar')
    hits = e.get_attribute('data-hits').replace(',', '').strip()
    total_pages = int(math.ceil(int(hits) / 100))

    for i in range(2):
        # e = wait.until(EC.presence_of_element_located((By.ID, 'selectAll')))
        # e.find_element_by_tag_name('input').click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectAll"]/input'))).click()

        _, _, file_count_before = next(os.walk(download_path))  # Count files in downloads
        driver.execute_script("viewProcessing('../pps/default.aspx?pp=RTF&amp;ppstype=Article',true)")  # Download RTF

        # Check for recaptcha
        if i > 0:
            # Load Captcha Frame
            # wait.until(EC.frame_to_be_available_and_switch_to_it(
            #     (By.XPATH, "//*[starts-with(@name, 'a-') and starts-with(@src, 'https://www-google-com')]")
            # ))
            wait.until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[src^='https://www-google-com.libproxy.wlu.ca/recaptcha/api2/anchor']")
            ))
            driver.implicitly_wait(random.uniform(0.5, 1.0))
            # Click the checkbox
            wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "span#recaptcha-anchor")
            )).click()
            driver.implicitly_wait(random.uniform(1.9, 2.98))
            # Switch back to main window
            driver.switch_to.parent_frame()

            #frame_idx = -1
            frames = driver.find_elements_by_tag_name('iframe')
            driver.switch_to.frame(5)
            driver.implicitly_wait(random.uniform(0.5, 1.9))
            driver.find_element_by_id('recaptcha-audio-button').click()

            # for idx, frame in enumerate(driver.find_elements_by_tag_name('iframe')):
            #     driver.switch_to.default_content()
            #     driver.switch_to.frame(frame)
            #     driver.implicitly_wait(random.uniform(1.53, 2.51))
            #     try:
            #         btn = driver.find_element_by_id('recaptcha-audio-button')
            #         btn.click()
            #         frame_idx = idx
            #     except Exception as e:
            #         print(e)
            #         pass
            # print(idx)
            # break

            # Load Captcha Challenge Frame
            # wait.until(EC.frame_to_be_available_and_switch_to_it(
            #     (By.CSS_SELECTOR, "iframe[title='recaptcha challenge']")
            # ))
            # # Click Audio Challenge
            # wait.until(EC.element_to_be_clickable(
            #     (By.CSS_SELECTOR, 'button#recaptcha-audio-button")]')
            # )).click()
            # Download Audio Challenge
            #wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'rc-audiochallenge-tdownload-link'))).click()


            # main_window = driver.current_window_handle
            # e = wait.until(EC.visibility_of_element_located((By.ID, 'nlmain__overlay')))
            # iframes = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe')))
            # recaptcha_frame = iframes[2]
            # driver.switch_to.frame(recaptcha_frame)
            # body = driver.find_element_by_xpath('/html/body')
            # print(body.get_attribute('innerHTML'))
            # print(body.get_attribute('innerText'))
            # print(body.get_attribute('text'))
            # checkbox = body.find_element_by_xpath('//*[@id="rc-anchor-alert"]')
            # print(checkbox.get_attribute('class'))

            #
            # checkbox = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rc-anchor-content')))
            # wait_between(0.5, 1.0)
            # checkbox.click()
            # print('click')
            # driver.switch_to.window(main_window)
            # driver.switch_to.default_content()
            # e.find_element_by_id('recaptcha-anchor').click()
            # e = wait.until(EC.presence_of_element_located((By.ID, 'recaptcha-audio-button')))
            # e.click()
            # e = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rc-audiochallenge-tdownload-link')))
            # e.click()

        # Wait for file download
        start_time = time.time()
        while True:
            time.sleep(5)
            _, _, file_count_after = next(os.walk(download_path))
            if file_count_after > file_count_before or (time.time() - start_time) > download_timeout:
                break

        wait_between(4.2, 5.3)

        # Go to next page - this takes a while
        # e = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'nextItem')))
        # e.click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="clearAll"]/input'))).click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="headlineHeader33"]/table/tbody/tr/td/a'))
        ).click()
        wait.until(EC.invisibility_of_element_located((By.ID, '_ceprogressindicator')))

        # driver.find_element_by_xpath('//*[@id="headlineHeader33"]/table/tbody/tr/td/a').click()
        # driver.find_element_by_xpath('//*[@id="clearAll"]/input').click()  # Clear list
