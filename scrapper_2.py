import requests
from bs4 import BeautifulSoup
from flask import Flask


def search_incruit(keyword, page=1):

    jobs = []
    for i in range(page):
        page = 30 * (i)
        url_2 = f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}&startno={page}"
        r_2 = requests.get(url_2)

        soup_2 = BeautifulSoup(r_2.text, "html.parser")
        lis_2 = soup_2.find_all("li", class_="c_col")
   

        for li_2 in lis_2:
            c_2 = li_2.find("a", class_="cpname").text
            t_2 = li_2.find("div", class_="cell_mid").find("div", class_="cl_top").find("a").text
            r_2 = li_2.find("div", class_="cl_md").find_all("span")[0].text
            l_2 = li_2.find("div", class_="cell_mid").find("div", class_="cl_top").find("a").get("href")
            d_2 = li_2.find('div', class_="cell_last").find("div", class_="cl_btm").find_all("span")[0].text
            job_data_2 = {
                "company": c_2,
                "title": t_2,
                "region": r_2,
                "link": l_2,
                "date": d_2
            }

            jobs.append(job_data_2)

    return(jobs)