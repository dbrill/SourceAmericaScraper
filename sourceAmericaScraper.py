#!/usr/local/bin/python3
import requests
import csv
from lxml import html

num_pages = 50
base_url = 'https://www.sourceamerica.org/nonprofit-locator?page='

def getCompanyName(html_tree: 'html.HtmlElement', row: int) -> str:
    name = html_tree.xpath(f'//*[@id="paragraph-966"]/div/div/div/div/div[{row}]/article/div/h6/span')
    if len(name) > 0:
        return name[0].text.replace(',', '')
    else:
        return ''


def getCompanyAddress(html_tree: 'html.HtmlElement', row: int) -> dict:
    street = html_tree.xpath(f'//*[@id="paragraph-966"]/div/div/div/div/div[{row}]/article/div/div/div[1]/p/span[1]')
    street = street[0].text if street else ''
    city = html_tree.xpath(f'//*[@id="paragraph-966"]/div/div/div/div/div[{row}]/article/div/div/div[1]/p/span[2]')
    city = city[0].text if city else ''
    state = html_tree.xpath(f'//*[@id="paragraph-966"]/div/div/div/div/div[{row}]/article/div/div/div[1]/p/span[3]')
    state = state[0].text if state else ''
    zip_code = html_tree.xpath(f'//*[@id="paragraph-966"]/div/div/div/div/div[{row}]/article/div/div/div[1]/p/span[4]')
    zip_code = zip_code[0].text if zip_code else ''

    return {'street': street, 'city': city, 'state': state, 'zip_code': zip_code}


def getCompanyNumber(html_tree: 'html.HtmlElement', row: int) -> str:
    number = html_tree.xpath(f'//*[@id="paragraph-966"]/div/div/div/div/div[{row}]/article/div/div/div[2]')
    if len(number) > 0:
        return number[0].text
    else:
        return ''


def getCompanySite(html_tree: 'html.HtmlElement', row: int) -> str:
    site = html_tree.xpath(f'//*[@id="paragraph-966"]/div/div/div/div/div[{row}]/article/div/div/div[3]/a')

    if len(site) > 0:
        return site[0].text
    else:
        return ''


def getCompany(html_tree: 'html.HtmlElement', row: int) -> dict:
    name = getCompanyName(html_tree, row)
    address = getCompanyAddress(html_tree, row)
    number = getCompanyNumber(html_tree, row)
    site = getCompanySite(html_tree, row)

    company = {'name': name, **address, 'number': number, 'site': site}
    return company


def getAllCompanies() -> list:
    companies = []
    for page in range(num_pages + 1):
        print(f'{{*}} Scraping Page: {page} {{*}}\n')
        res = requests.get(f'{base_url}{page}')
        tree = html.fromstring(res.content)
        for row in range(1, 13):
            company = getCompany(tree, row)
            companies.append(company)
    return companies


def writeCompanyData(companies: list):
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
