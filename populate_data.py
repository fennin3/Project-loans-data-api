import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','loan_data_project.settings')
django.setup()

from loan_app.models import Loan

# Using selenium to scrape 100 rows of the table data
def scrape_data():
    print("\nScraping 100 rows of data...")
    time.sleep(10)
    global driver
    
    # setting the pagination of the page to 100 items per page
    select = Select(driver.find_element(By.XPATH,'//select[@id="show-entries"]'))
    select.select_by_value('100')
    time.sleep(10)
    
    # collecting the list of table rows
    table_data = driver.find_elements(By.XPATH,"//div/article")
    print("Scraping Done --> 100%\n")
    return table_data

# Processing the collected data into list if dictionaries
def process_table_data(table_data):
    print("Data Processing...")
    del table_data[0]
    del table_data[-1]
    
    processed_dataset = []
    
    for row in table_data:
        row_data = str(row.text).split('\n')
        row_data = {
            "signature_date":row_data[0],
            "title":row_data[1],
            "country":row_data[2],
            "sector":row_data[3],
            "signed_amount":row_data[4]
        }
        processed_dataset.append(row_data)
    print("Data Processing Done --> 100%\n")
    return processed_dataset

# Creating database records from the list of dictionaries
def populate_database(dataset):
    print("Populating Database...")
    db_objects = []
    for data in dataset:
        db_objects.append(Loan(**data))
    
    Loan.objects.bulk_create(db_objects)
    print("Done --> 100%")


if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')        
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    url = "https://www.eib.org/en/projects/loans/index.htm"
    driver.get(url)
    driver.implicitly_wait(40)
    
    table_data = scrape_data()
    dataset = process_table_data(table_data)
    driver.quit()
    
    populate_database(dataset)

    