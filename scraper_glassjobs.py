from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import datetime
import pandas as pd
import csv
from datetime import datetime, timedelta
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def jobseleniumglassjobs():

    file=open('glassdoorJoobs.csv','w',encoding='utf-8',newline='')
    csv_writer=csv.writer(file)
    csv_writer.writerow(['Job Title' , 'Posted' ,'Salary' ,'WorkTime' ,'Link' ,'Location' ,'Source' ,'Extracted Date'])
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument('intl.accept_languages')
    options.add_argument('--lang=en-GB')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://www.glassdoor.co.uk/Job/index.htm")
    actions = ActionChains(driver)
    job_title_search = driver.find_element(By.CSS_SELECTOR ,'input#searchBar-jobTitle').send_keys(jobTitleQuery)
    sleep(2)
    job_location_search =driver.find_element(By.CSS_SELECTOR ,'input#searchBar-location').send_keys(location)
    actions.send_keys(Keys.ENTER)
    x=0
    while True:
        try:
            while True:
                try:
                    driver.find_element(By.CSS_SELECTOR,'h2[data-test="auth-entry-title"]')
                    sleep(1)
                    driver.find_element(By.CSS_SELECTOR,'button.e1jbctw80.ei0fd8p1.css-1n14mz9.e1q8sty40').click()
                    sleep(1)
                except:break

            li_elements = driver.find_elements(By.CSS_SELECTOR, 'li.JobsList_jobListItem__JBBUV')

            driver.execute_script("arguments[0].scrollIntoView();", li_elements[-1])
            print("passsed")
            sleep(1)
            for li_element in li_elements[x:]:
                job_title = "No"
                job_location = "No"
                job_salary = "No"
                job_link = "No"
                posted = "No"
                work_time = "No"
                source = "Glass door Jobs"
                extracteddate = datetime.datetime.now()
                try:
                    job_title = li_element.find_element(By.CSS_SELECTOR, 'a[id*="job-title-"]').text
                except:
                    pass
                try:
                    job_location = li_element.find_element(By.CSS_SELECTOR, 'div[id*="job-location-"]').text
                except:
                    pass
                try:
                    job_salary = li_element.find_element(By.CSS_SELECTOR, 'div[id*="job-salary-"]').text
                except:
                    pass
                try:
                    job_link = li_element.find_element(By.CSS_SELECTOR, 'a[data-test="job-link"]').get_attribute('href')
                except:
                    pass
                try:
                    posted = li_element.find_element(By.CSS_SELECTOR, 'div.d-flex.align-items-end.ml-xsm.listing-age').text
                except:
                    pass

                csv_writer.writerow(
                    [job_title, posted, job_salary, work_time, job_link, job_location, source, extracteddate])
            x+=20
            butt_next = driver.find_element(By.CSS_SELECTOR, 'div[class*="JobsList_buttonWrapper__"]').find_element(
                By.CSS_SELECTOR, 'button[class*="button_Button__meEg5 button-base_Button__"]')
            butt_next.click()
            sleep(3)

        except:
            print("Scraping finished Succefully")
            break


    file.close()
    main_data_frame = pd.read_csv("glassdoorJoobs.csv")
    writer = pd.ExcelWriter(r'glassdoor_jobs_excel_data.xlsx', engine='xlsxwriter')

    main_data_frame.to_excel(writer, index=False)
    writer.close()