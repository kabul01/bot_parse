import random
import re

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker

from db import engine, TaskCodeForces

Session = sessionmaker(bind=engine)
session = Session()

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]
headers = {"User-Agent": user_agent_list[random.randint(0, len(user_agent_list) - 1)]}

for n in range(1, 87):

    url = f"https://codeforces.com/problemset/page/{n}?order=BY_SOLVED_DESC"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    titles = soup.select('div[style="float: left;"]')
    numbers = soup.select('td[class="id"]')
    topics = soup.select('div[style="float: right; font-size: 1.1rem; padding-top: 1px; text-align: right;"]')
    complexitys = soup.select('td[style="font-size: 1.1rem"]')
    count_solutions = soup.select('td[style="font-size: 1.1rem;"]')

    for number, title, topic_task, count_solution, complexity in zip(numbers, titles, topics, count_solutions,
                                                                     complexitys):
        chars = re.findall(r'[a-zA-Z]+', number.find('a', href=True).text.strip().replace("\n", ''))
        nums = re.findall(r'\d+', number.find('a', href=True).text.strip().replace("\n", ''))
        for num in nums:
            for char in chars:
                if not len(nums) >= 2:
                    task_url = f"https://codeforces.com/problemset/problem/{num}/{char}"
                else:
                    task_url = f"https://codeforces.com/problemset/problem/{num}/{char}{nums[1]}"
        tasks = [
            TaskCodeForces(
                number=number.find('a', href=True).text.strip().replace("\n", ''),
                title=title.text.replace(" ", "").strip(),
                topic_task=topic_task.text.replace(" ", '').strip(),
                count_solution=count_solution.text.replace(" ", "").strip(),
                complexity=complexity.text.replace(" ", "").strip(),
                url=task_url)

        ]
        session.add_all(tasks)
        session.commit()
print("finish!")

# def get_url():
#     for count in range(1, 8):
#         sleep(1)
#         url = f"https://scrapingclub.com/exercise/list_basic/?page={count}"
#
#         response = requests.get(url, headers=headers)
#         print(response.status_code)
#         # print(response.text)
#
#
#         soup = BeautifulSoup(response.text, "lxml")
#         data = soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")
#         for i in data:
#             card_url = "https://scrapingclub.com" + i.find("a").get("href")
#             yield card_url
#
#
# for card_url in get_url():
#     response = requests.get(card_url, headers=headers)
#     soup = BeautifulSoup(response.text, "lxml")
#     data = soup.find("div", class_="card mt-4 my-4")
#     name = data.find("h3", class_="card-title").text
#     price = data.find("h4").text
#     desc = data.find("p", class_="card-text").text
#     url_img = data.find("img", class_="card-img-top img-fluid").get("src")
#     print(name + "\n" + price + "\n" + desc + "\n" + url_img)
#
#     data = soup.find("table", class_="problems")
#     tasks = data.find_all("tr")
# print(soup.select('div[style="float: left;"]'))
# print(soup.select('div[style="float: right; font-size: 1.1rem; padding-top: 1px; text-align: right;"]'))
# for i in soup.select('div[style="float: left;"]'):
#     print(i.find("a").text)
# # print(soup.select('td[style="font-size: 1.1rem"]'))
# for i in soup.select('td[style="font-size: 1.1rem"]'):
#     print(i.find("span", class_="ProblemRating").text)

# for i in soup.select('div[style="float: right; font-size: 1.1rem; padding-top: 1px; text-align: right;"]'):
#     print(i.find("a", class_="notice").text)
# url = f"https://codeforces.com/problemset/page/{2}?order=BY_SOLVED_DESC"
# response = requests.get(url, headers=headers)
# # soup = BeautifulSoup(response.text, "lxml")
# for n in range(1, 3):

#
#     titles = soup.select('div[style="float: left;"]')
#     numbers = soup.select('td[class="id"]')
#     topics = soup.select('div[style="float: right; font-size: 1.1rem; padding-top: 1px; text-align: right;"]')
#     complexitys = soup.select('td[style="font-size: 1.1rem"]')
#     count_solutions = soup.select('td[style="font-size: 1.1rem;"]')
#
# url = f"https://codeforces.com/problemset/page/{2}?order=BY_SOLVED_DESC"
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "lxml")
# numbers = soup.select('td[class="id"]')
# for i in numbers:
#     print(i.find('a', href=True).text.strip())
