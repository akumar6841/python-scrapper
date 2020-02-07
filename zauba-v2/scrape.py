#Program to extract company details from zaubacorp

#Import required libraries

#Pandas: to work with dataframes
import pandas as pd

#Requests: to send http request to server
import requests

#BeautifulSoup: to extract data from html
from bs4 import BeautifulSoup

import json
import os


#Function to slugify string
def slugify(s1):
    s2 = s1.replace(" ", "-")
    s3 = s2.replace(". ","-")
    s4 = s3.replace(".","-")
    return s4




f = "./data.csv"

if os.path.exists(f):
    df = pd.read_csv(f)
else:
    df = pd.DataFrame(columns=["CIN", "Company Name", "Company Status", "ROC Code", "Registration Number", "Company Category", "Company Sub Category",
         "Class of Company", "Date of Incorporation", "Age of Company", "Authorised Capital", "Paid Up Capital", "Listing status",
          "Date of Last Annual General Meeting", "Date of Latest Balance Sheet", "Email Id",  "Address", "URL"])  


#Create DataFrame with below columns


with open('status.json') as file:
    data = json.load(file)


fetched_page = data['status'][0].get('fetched_page')


last_page = 13333


#Loop for pages
for i in range(fetched_page+1, last_page+1):
    
    print("-------Fetching data for page :", i, '-----------')
    
    page_url = "https://www.zaubacorp.com/company-list/p-"+str(i)+"-company.html";
    
    company_list_page = requests.get(page_url)
    
    soup = BeautifulSoup(company_list_page.content, 'html5lib')
    
    company_list_table = soup.find('table', attrs = {'id':'table'}).find('tbody')

    row_length = len(company_list_table.findAll('tr'))


    with open('status.json') as file:
        data = json.load(file)


    fetched_row = data['status'][0].get('fetched_row')

    
    #Loop for rows in a page
    for j in range(fetched_row+1, row_length+1):
 

        print("Fetching data for row : ", j, " at page ", i)

        row = company_list_table.findAll('tr')[j-1]

        record = row.findAll('td')
        
        CIN = record[0].text

        CompanyName = record[1].find('a').text

        
        company_page_url = "https://www.zaubacorp.com/company/"+slugify(CompanyName)+"/" + CIN

    
        
        company_page = requests.get(company_page_url)
        
        if company_page.status_code==200:
            
            soup2 = BeautifulSoup(company_page.content, 'html5lib')
            
            table = soup2.findAll('table')[0] #company detail table
            
            table2 = soup2.findAll('table')[3] #capital table
            
            table3 = soup2.findAll('table')[4] #date table
            
            info = soup2.findAll('div', attrs = {'class': 'col-12'})[0] #email, address section
            
            Email = info.findAll('p')[0].text.split(' ')[3]

            Address = info.findAll('p')[3].text
            
            ListingStatus = table3.find('thead').findAll('tr')[0].findAll('td')[1].find('p').text
            
            DateOfLastAnnualGeneralMeeting = table3.find('tbody').findAll('tr')[0].findAll('td')[1].find('p').text
            
            DateOfLatestBalanceSheet = table3.find('tbody').findAll('tr')[1].findAll('td')[1].find('p').text
     
            AuthorizedCapital = table2.find('tbody').findAll('tr')[0].findAll('td')[1].find('p').text
        
            PaidUpCapital = table2.find('tbody').findAll('tr')[1].findAll('td')[1].find('p').text
            
            CIN = table.find('thead').findAll('tr')[0].findAll('td')[1].find('a').text
            
            CompanyName = table.find('tbody').findAll('tr')[0].findAll('td')[1].find('p').text
            
            CompanyStatus = table.find('tbody').findAll('tr')[1].findAll('td')[1].find('p').text
            
            RoC = table.find('tbody').findAll('tr')[2].findAll('td')[1].find('p').text
            
            RegistrationNumber = table.find('tbody').findAll('tr')[3].findAll('td')[1].find('p').text
            
            CompanyCategory = table.find('tbody').findAll('tr')[4].findAll('td')[1].find('p').text
            
            CompanySubCategory = table.find('tbody').findAll('tr')[5].findAll('td')[1].find('p').text
            
            ClassOfCompany = table.find('tbody').findAll('tr')[6].findAll('td')[1].find('p').text
            
            DateOfIncorporation = table.find('tbody').findAll('tr')[7].findAll('td')[1].find('p').text
            
            AgeOfCompany = table.find('tbody').findAll('tr')[8].findAll('td')[1].find('p').text
            
            row = {
                'CIN' : CIN,
                'Company Name': CompanyName,
                'Company Status': CompanyStatus,
                'ROC Code' : RoC,
                'Registration Number': RegistrationNumber,
                'Company Category': CompanyCategory,
                'Company Sub Category': CompanySubCategory,
                'Class of Company' : ClassOfCompany,
                'Date of Incorporation': DateOfIncorporation,
                'Age of Company' : AgeOfCompany,
                'Authorised Capital': AuthorizedCapital,
                'Paid Up Capital': PaidUpCapital,
                'Listing status': ListingStatus,
                'Date of Last Annual General Meeting': DateOfLastAnnualGeneralMeeting,
                'Date of Latest Balance Sheet': DateOfLatestBalanceSheet,
                'Email Id': Email,
                'Address': Address,
                'URL' : company_page_url
            }
            
            df = df.append(row , ignore_index=True)
            df.to_csv('data.csv', encoding='utf-8')

            data = {}
            data['status'] = []
            data['status'].append({
                'fetched_page': i-1,
                'fetched_row': j
            })

            with open('status.json', 'w') as outfile:
                json.dump(data, outfile)
            
            
          
        else:
            
            print("Page not found : ",company_page_url)

    data = {}
    data['status'] = []
    data['status'].append({
        'fetched_page': i,
        'fetched_row': 0
    })
    with open('status.json', 'w') as outfile:
        json.dump(data, outfile)          
     

print("Process Completed");

