import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv


def pharse(browser):
    rank = [item.text for item in browser.find_elements(By.CSS_SELECTOR,
                                                        '#content-box > div.rk-table-box > table > tbody td:nth-child(1) > div')]
    name = [item.text for item in browser.find_elements(By.CSS_SELECTOR,
                                                        '#content-box > div.rk-table-box > table > tbody td.align-left > div > div.tooltip > div > a > span')]
    region = [item.get_attribute('style')[50:52] for item in browser.find_elements(By.CSS_SELECTOR,
                                                                                   '#content-box > div.rk-table-box > table > tbody td:nth-child(3) > div')]
    regional_rank = [item.text for item in browser.find_elements(By.CSS_SELECTOR,
                                                                 '#content-box > div.rk-table-box > table > tbody td:nth-child(4)')]
    total_score = [item.text for item in browser.find_elements(By.CSS_SELECTOR,
                                                               '#content-box > div.rk-table-box > table > tbody  td:nth-child(5)')]
    alumni = [item.text for item in
              browser.find_elements(By.CSS_SELECTOR, '#content-box > div.rk-table-box > table > tbody td:nth-child(6)')]
    button = browser.find_element(By.CSS_SELECTOR,
                                  '#content-box > div.rk-table-box > table > thead > tr > th:nth-child(6) > div > div.rank-select > div.inputWrapper > input')
    button.click()
    button = browser.find_element(By.CSS_SELECTOR,
                                  '#content-box > div.rk-table-box > table > thead > tr > th:nth-child(6) > div > div.rank-select > div.rk-tooltip > ul > li:nth-child(2)')
    button.click()
    award = [item.text for item in
             browser.find_elements(By.CSS_SELECTOR, '#content-box > div.rk-table-box > table > tbody td:nth-child(6)')]
    button = browser.find_element(By.CSS_SELECTOR,
                                  '#content-box > div.rk-table-box > table > thead > tr > th:nth-child(6) > div > div.rank-select > div.inputWrapper > input')
    button.click()
    button = browser.find_element(By.CSS_SELECTOR,
                                  '#content-box > div.rk-table-box > table > thead > tr > th:nth-child(6) > div > div.rank-select > div.rk-tooltip > ul > li:nth-child(3)')
    button.click()
    Hici = [item.text for item in
            browser.find_elements(By.CSS_SELECTOR, '#content-box > div.rk-table-box > table > tbody td:nth-child(6)')]
    button = browser.find_element(By.CSS_SELECTOR,
                                  '#content-box > div.rk-table-box > table > thead > tr > th:nth-child(6) > div > div.rank-select > div.inputWrapper > input')
    button.click()
    button = browser.find_element(By.CSS_SELECTOR,
                                  '#content-box > div.rk-table-box > table > thead > tr > th:nth-child(6) > div > div.rank-select > div.rk-tooltip > ul > li:nth-child(4)')
    button.click()
    NS = [item.text for item in
          browser.find_elements(By.CSS_SELECTOR, '#content-box > div.rk-table-box > table > tbody td:nth-child(6)')]
    button = browser.find_element(By.CSS_SELECTOR,
                                  '#content-box > div.rk-table-box > table > thead > tr > th:nth-child(6) > div > div.rank-select > div.inputWrapper > input')
    button.click()
    button = browser.find_element(By.CSS_SELECTOR,
                                  '#content-box > div.rk-table-box > table > thead > tr > th:nth-child(6) > div > div.rank-select > div.rk-tooltip > ul > li:nth-child(5)')
    button.click()
    PUB = [item.text for item in
           browser.find_elements(By.CSS_SELECTOR, '#content-box > div.rk-table-box > table > tbody td:nth-child(6)')]
    button = browser.find_element(By.CSS_SELECTOR,
                                  '#content-box > div.rk-table-box > table > thead > tr > th:nth-child(6) > div > div.rank-select > div.inputWrapper > input')
    button.click()
    button = browser.find_element(By.CSS_SELECTOR,
                                  '#content-box > div.rk-table-box > table > thead > tr > th:nth-child(6) > div > div.rank-select > div.rk-tooltip > ul > li:nth-child(6)')
    button.click()
    PCP = [item.text for item in
           browser.find_elements(By.CSS_SELECTOR, '#content-box > div.rk-table-box > table > tbody td:nth-child(6)')]
    list = [{'Rank': item1,
             'Name': item2,
             'Region': item3,
             'Regional rank': item4,
             'Total score': item5,
             'Alumni': item6,
             'Award': item7,
             'Hici': item8,
             'N&S': item9,
             'PUB': item10,
             'PCP': item11
             }
            for item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11 in
            zip(rank, name, region, regional_rank, total_score, alumni, award, Hici, NS, PUB, PCP)]
    return list
def main():
    url = 'https://www.shanghairanking.com/rankings/arwu/2023'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1920x3000")
    chrome_options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)

    with open('../data/Shanghai_ranking_data_2023.csv', 'w', newline='') as csvfile:
        fieldnames = ['Rank', 'Name', 'Region', 'Regional rank', 'Total score',
                      'Alumni', 'Award', 'Hici', 'N&S', 'PUB',
                      'PCP']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(33):
            for item in pharse(browser):
                writer.writerow(item)
            button = browser.find_element(By.CSS_SELECTOR, '#content-box > ul > li.ant-pagination-next > a')
            button.click()



main()
