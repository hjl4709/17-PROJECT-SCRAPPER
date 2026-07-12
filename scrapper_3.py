import requests
from bs4 import BeautifulSoup
from flask import Flask

headers_1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Sec-Fetch-Mode': 'navigate',
}


jobs = []
url_2 = f"https://www.jobkorea.co.kr/Search?stext=간호사&tabType=recruit&Page_No=1"
r_2 = requests.get(url_2, headers=headers_1)
soup_2 = BeautifulSoup(r_2.text, "html.parser")
lis_2 = soup_2.find_all("div", class_="flex flex-col")


for li_2 in lis_2:
    c = li_2.find("span", class_="truncate text-gray700 text-typo-b2-16")
    t = li_2.find("span", class_="truncate font-semibold text-typo-b1-18 text-gray900")
    r = li_2.find("span", class_="truncate text-gray900 text-typo-b4-14")
    l = li_2.find("a").get("href")
    d = li_2.find("span", class_="text-typo-c1-13 text-gray700")

    if c and t:
        c_2 = c.text.strip()
        t_2 = t.text.strip()
        r_2 = r.text.strip()
        l_2 = l
        d_2 = d

        print(c_2)
        print(t_2)
        print(r_2)
        print(l_2)
        print(d_2)
        print("-" * 40)

