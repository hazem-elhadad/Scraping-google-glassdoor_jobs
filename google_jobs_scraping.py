import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import datetime

file=open('Joobssoup.csv','w',encoding='utf-8',newline='')
csv_writer=csv.writer(file)
csv_writer.writerow(['Job Title' , 'Posted' ,'Salary' ,'WorkTime' ,'Link' ,'Location' ,'Source' ,'Extracted Date'])
for i in range (0,160):
    i+=20
    url = f"https://www.google.com/search?vet=10ahUKEwju06X1h-WBAxWqVKQEHXhxCXIQ06ACCN4M..i&ei=7uUhZYzBF7-okdUPpMSbyAo&opi=89978449&yv=3&rciv=jb&nfpr=0&q=react+jobs+in+london+uk&start={i}&asearch=jb_list&cs=1&async=_id:VoQFxe,_pms:hts,_fmt:pc"

    payload = {}
    headers = {
      'authority': 'www.google.com',
      'accept': '*/*',
      'accept-language': 'en-GB,en;q=0.9',
      'cookie': 'AEC=Ackid1Rr_hG8AwGT5hHHrubxwIySIbUX22MLc_eqjj59IgZFkfxNLox5SfQ; SEARCH_SAMESITE=CgQItZkB; 1P_JAR=2023-10-07-19; NID=511=iewTZmadOm9miV24iNI_O9GuEmYkZkTJ8YKMSUYDMD0_NkmyC4j8vqskbO5QZJMEyMubX3xF5YFDIkODEL0kLXP2VhIM5_1SheC4IxZl8dlCmBno63Ep9A-3HI_A9en5kReQSp14RmA45gxCsAwrTwEIkSF6rwLRYxrGbFaReJ-x_6frgyYR86sVe-QXxiQo08Vt-1zRIilzEF7qpw5SBj6MbHBlydQeamMfn2f5LOuDVxvXzJqg0RPHvnYts5CAWA; DV=s5aQa73W8EY6IEANI_VkzuAr48C6sNiTQjqbJ61vTdgAAFDfwJQCpgYXmDYAAAA; 1P_JAR=2023-10-07-19',
      'referer': 'https://www.google.com/',
      'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
      'sec-ch-ua-arch': '"x86"',
      'sec-ch-ua-bitness': '"64"',
      'sec-ch-ua-full-version': '"117.0.5938.149"',
      'sec-ch-ua-full-version-list': '"Google Chrome";v="117.0.5938.149", "Not;A=Brand";v="8.0.0.0", "Chromium";v="117.0.5938.149"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-model': '""',
      'sec-ch-ua-platform': '"Windows"',
      'sec-ch-ua-platform-version': '"10.0.0"',
      'sec-ch-ua-wow64': '?0',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
      'x-client-data': 'CJW2yQEIprbJAQipncoBCPrrygEIlKHLAQib/swBCIWgzQEI3L3NAQiSys0BCLnKzQEIvNDNAQjF0c0BCPfTzQEI0tbNAQio2M0BCPnA1BUY9cnNARi60s0B'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    soup = BeautifulSoup(response.text, 'lxml')
    list_of_li=soup.findAll('li')

    for ele1 in list_of_li:
        job_title="No"
        posted="No"
        salary="No"
        work_time="No"
        location="No"
        source= "Google Jobs"
        extracteddate = datetime.datetime.now()
        link="No"
        job_datail = ele1.find("div", {"class": "KKh3md"}).findAll('div')
        for det in job_datail:
            if any(chr.isdigit() for chr in det.text) and "UK£" not in det.text:
                posted=det.text
            if ("US$" in det.text or "UK£") and "دوام" not in det.text and "قبل" not in det.text and "متعاقد" not in det.text:
                salary = det.text
            else:
                work_time = det.text
        job_title=ele1.find("div", {"class": "BjJfJf PUpOsf"}).text
        link=ele1.find("div", {"class": "PwjeAc"}).find("div", {"class": "lR4X6c"}).findNext('div').findNext('div').findNext('div')['data-share-url']
        location = ele1.find("div", {"class": "oNwCmf"}).find("div", {"class": "Qk80Jf"}).text
        csv_writer.writerow([job_title, posted,salary,work_time,link, location,source,extracteddate])

file.close()
main_data_frame = pd.read_csv("Joobssoup.csv")
writer = pd.ExcelWriter(r'jobs_excel_data.xlsx', engine='xlsxwriter')

main_data_frame.to_excel(writer, index=False)
writer.close()


