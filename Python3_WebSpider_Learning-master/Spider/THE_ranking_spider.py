# To use this script please make sure you have installed the browser version of 'chromedrive' and placed it in the correct location
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def parse_ranking_page(html):
    pattern = re.compile('role="row".*?sorting_2.*?>(.*?)</td>.*?title.*?>(.*?)</a>.*?stats_number_students.*?>(.*?)</td>.*?stats_student_staff_ratio.*?>(.*?)</td>.*?stats_pc_intl_students.*?>(.*?)</td>.*?stats_female_male_ratio.*?>(.*?)</td>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {'RankTHE': item[0],
               'Name': item[1],
               'No. of FTE students': item[2],
               'No. of students per staff': item[3],
               'International Students': item[4],
               'Female:Male Ratio': item[5]
               }


def parse_scores_page(html):
    pattern = re.compile('role="row".*?sorting_2.*?>.*?</td>.*?title.*?>(.*?)</a>.*?overall-score.*?>(.*?)</td>.*?teaching-score.*?>(.*?)</td>.*?research-score.*?>(.*?)</td>.*?citations-score.*?>(.*?)</td>.*?industry_income-score.*?>(.*?)</td>.*?international_outlook-score.*?>(.*?)</td>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {'Name': item[0],
               'Overall': item[1],
               'Teaching': item[2],
               'Research Environment': item[3],
               'Research Quality': item[4],
               'Industry': item[5],
               'International Outlook': item[6]
               }


def main():
    url = 'https://www.timeshighereducation.com/world-university-rankings/2023/world-ranking#!/length/-1/sort_by/rank/sort_order/asc/cols/stats'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1920x3000")
    chrome_options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    html_ranking = browser.page_source
    scores = browser.find_element(By.CSS_SELECTOR, '#block-system-main > div > div.container > div > div.col-sm-8.content-primary > div.panel-pane.pane-the-data-rankings-datatables > div > div.toggle-cols > ul > li:nth-child(2) > label')
    scores.click()
    html_scores = browser.page_source
    with open('THE_ranking_data.csv', 'a', newline='') as csvfile:
        fieldnames = ['RankTHE', 'Name', 'No. of FTE students', 'No. of students per staff', 'International Students',
                      'Female:Male Ratio', 'Overall', 'Teaching', 'Research Environment', 'Research Quality',
                      'Industry', 'International Outlook']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item_ranking in parse_ranking_page(html_ranking):
            for item_scores in parse_scores_page(html_scores):
                if item_ranking['Name'] == item_scores['Name']:
                    item_ranking.update(item_scores)
                    print(item_ranking)
                    writer.writerow(item_ranking)
                    print(f'Donnees ecrites pour {item_ranking["Name"]}')
    browser.close()


main()
