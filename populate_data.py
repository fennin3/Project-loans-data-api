import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import django
from datetime import datetime
from decimal import Decimal


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loan_data_project.settings")
django.setup()

from loan_app.models import Loan, Country, Sector, Currency

# Processing the collected data into list if dictionaries
def process_table_data(table_data):
    print("Data Processing...")

    loan_dataset = []

    for row in table_data[1:-1]:
        """Splitting eact data row into a list
        index 0 = signature_date
        index 1 = title
        index 2 = country
        index 3 = sector
        index 4 = signed_amount
        """
        row_data = str(row.text).split("\n")
        # converting str to date format
        formatted_date = datetime.strptime(row_data[0].strip(), "%d %B %Y")
        # Removing the currency symbol the prefix the text
        amount = Decimal(str(row_data[4][1:]).strip().replace(",", ""))
        # Slicing the first character (the currency symbol)
        currency = row_data[4][0]

        loan_dataset.append(
            {
                "signature_date": formatted_date,
                "title": row_data[1],
                "country": row_data[2].strip(),
                "sector": row_data[3],
                "signed_amount": amount,
                "currency": currency,
            }
        )

    print("Data Processing Done --> 100%\n")
    return loan_dataset


# Creating database records from the list of dictionaries
def populate_database(dataset):
    print("Populating Database...")
    countries = []
    sectors = []
    currencies = []

    for country in set([data["country"] for data in dataset]):
        countries.append(Country(name=country))

    for sector in set([data["sector"] for data in dataset]):
        sectors.append(Sector(name=sector))

    for currency in set([data["currency"] for data in dataset]):
        currencies.append(Currency(symbol=currency))

    Country.objects.bulk_create(countries)
    Sector.objects.bulk_create(sectors)
    Currency.objects.bulk_create(currencies)
    loan_objs = []

    for data in dataset:
        loan_objs.append(
            Loan(
                title=data["title"],
                signature_date=data["signature_date"],
                signed_amount=data["signed_amount"],
                sector=Sector.objects.get(name=data["sector"]),
                country=Country.objects.get(name=data["country"]),
                currency=Currency.objects.get(symbol=data["currency"]),
            )
        )

    Loan.objects.bulk_create(loan_objs)
    print("Done --> 100%")


if __name__ == "__main__":

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    url = "https://www.eib.org/en/projects/loans/index.htm"
    driver.get(url)
    driver.implicitly_wait(40)

    print("\nScraping 100 rows of data...")
    time.sleep(10)

    # setting the pagination of the page to 100 items per page
    select = Select(driver.find_element(By.XPATH, '//select[@id="show-entries"]'))
    select.select_by_value("100")
    time.sleep(10)

    # collecting the list of table rows (100)
    table_data = driver.find_elements(By.XPATH, "//div/article")
    print("Scraping Done --> 100%\n")

    dataset = process_table_data(table_data)
    driver.quit()

    populate_database(dataset)
