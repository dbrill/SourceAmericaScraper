#!/usr/local/bin/python3
import requests
import csv
from lxml import html
pages = 60

base_url = 'https://www.sourceamerica.org/nonprofit-locator?page='


def getCompanyName(html_tree: 'html.HtmlElement', row: int) -> str:
    name = html_tree.xpath(f'//*[@id="block-views-affiliates-block-1"]/div/div/div/div[2]/div/div[1]/div[{row}]\
    /strong/text()')
    if len(name) > 0:
        return name[0]
    else:
        return ''


def getCompanyAddress(html_tree: 'html.HtmlElement', row: int) -> dict:
    street = html_tree.xpath(f'//*[@id="block-views-affiliates-block-1"]/div/div/div/div[2]/div/div[1]/div[{row}]\
    /div[1]/div/div/div[1]/div/text()')
    street = street[0] if street else ''
    city = html_tree.xpath(f'//*[@id="block-views-affiliates-block-1"]/div/div/div/div[2]/div/div[1]/div[{row}]\
    /div[1]/div/div/div[2]/span[1]/text()')
    city = city[0] if city else ''
    state = html_tree.xpath(f'//*[@id="block-views-affiliates-block-1"]/div/div/div/div[2]/div/div[1]/div[{row}]\
        /div[1]/div/div/div[2]/span[2]/text()')
    state = state[0] if state else ''
    zip_code = html_tree.xpath(f'//*[@id="block-views-affiliates-block-1"]/div/div/div/div[2]/div/div[1]/div[{row}]\
        /div[1]/div/div/div[2]/span[3]/text()')
    zip_code = zip_code[0] if zip_code else ''

    return {'street': street, 'city': city, 'state': state, 'zip_code': zip_code}


def getCompanyNumber(html_tree: 'html.HtmlElement', row: int) -> str:
    number = html_tree.xpath(f'//*[@id="block-views-affiliates-block-1"]/div/div/div/div[2]/div/div[1]/div[{row}]\
    /div[2]/div/div/text()')
    if len(number) > 0:
        return number[0]
    else:
        return ''


def getCompanySite(html_tree: 'html.HtmlElement', row: int) -> str:
    site = html_tree.xpath(f'//*[@id="block-views-affiliates-block-1"]/div/div/div/div[2]/div/div[1]/div[{row}]\
    /div[3]/div/div/a/text()')
    if len(site) > 0:
        return site[0]
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
    for page in range(60):
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
