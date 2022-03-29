import requests
import csv
from lxml import html
from typing import List

num_pages = 50
base_url = 'https://www.sourceamerica.org/nonprofit-locator?page='

RAW_BLOCK_CLASS = "views-row"
ADDRESS_1_CLASS = "address-line1"
ADDRESS_2_CLASS = "address-line2"
CITY_CLASS = "locality"
STATE_CLASS = "administrative-area"
ZIP_CODE_CLASS = "postal-code"
COUNTRY_CLASS = "country"

def getElementTextSafe(elem: List['html.HtmlElement']) -> str:
    res = ''
    try:
        res = elem[0].text.replace(',', '')
    except IndexError:
        pass

    return res


def getCompanyName(company_block: 'html.HtmlElement') -> str:
    return getElementTextSafe(company_block.cssselect("h6 > span"))


def getCompanyAddress(company_block: 'html.HtmlElement') -> dict:
    addr_1 = getElementTextSafe(company_block.find_class(ADDRESS_1_CLASS))
    addr_2 = getElementTextSafe(company_block.find_class(ADDRESS_2_CLASS))
    street = f"{addr_1} : {addr_2}" if addr_2 != "" else addr_1
    city = getElementTextSafe(company_block.find_class(CITY_CLASS))
    state = getElementTextSafe(company_block.find_class(STATE_CLASS))
    zip_code = getElementTextSafe(company_block.find_class(ZIP_CODE_CLASS))

    return {'street': street, 'city': city, 'state': state, 'zip_code': zip_code}


def getCompanyNumber(company_block: 'html.HtmlElement') -> str:
    number = ''
    try:
        number = company_block.find_class('text-16')[0].find_class('my-15')[1].text
    except IndexError:
        pass
    return number


def getCompanySite(company_block: 'html.HtmlElement') -> str:
    return getElementTextSafe(company_block.cssselect('a'))


def getCompany(company_block: 'html.HtmlElement') -> dict:
    name = getCompanyName(company_block)
    address = getCompanyAddress(company_block)
    number = getCompanyNumber(company_block)
    site = getCompanySite(company_block)

    company = {'name': name, **address, 'number': number, 'site': site}
    return company


def getAllCompanies() -> List[dict]:
    companies = []
    for page in range(num_pages + 1):
        print(f'{{*}} Scraping Page: {page} {{*}}')
        res = requests.get(f'{base_url}{page}')
        tree = html.fromstring(res.content)
        raw_company_blocks = tree.find_class(RAW_BLOCK_CLASS)
        for block in range(12):
            try:
                company = getCompany(raw_company_blocks[block])
                companies.append(company)
            except IndexError:
                print(f"Exceeded number of company blocks for page: {page}\tblock: {block}")
    return companies


def writeCompanyData(companies: List[dict]) -> None:
    filename = 'sourceAmericaData.csv'
    print(f'[!] WRITING DATA TO: {filename}')
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = list(companies[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company_data in companies:
            writer.writerow(company_data)


companies = getAllCompanies()
writeCompanyData(companies)
