import requests
from bs4 import BeautifulSoup
from flask import Flask

def search_incruit(keyword, page=1):
    headers_1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Sec-Fetch-Mode': 'navigate',
    }

    jobs = []

    # 인크루트
    for i in range(page):
        page = 30 * (i)
        url_1 = f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}&startno={page}"
        r_1 = requests.get(url_1)

        soup_1 = BeautifulSoup(r_1.text, "html.parser")
        lis_1 = soup_1.find_all("li", class_="c_col")
   

        for li_1 in lis_1:
            c_1 = li_1.find("a", class_="cpname").text
            t_1 = li_1.find("div", class_="cell_mid").find("div", class_="cl_top").find("a").text
            r_1 = li_1.find("div", class_="cl_md").find_all("span")[0].text
            l_1 = li_1.find("div", class_="cell_mid").find("div", class_="cl_top").find("a").get("href")
            d_1 = li_1.find('div', class_="cell_last").find("div", class_="cl_btm").find_all("span")[0].text

            job_data_1 = {
                "site": "인크루트",
                "company": c_1,
                "title": t_1,
                "region": r_1,
                "date": d_1,
                "link": l_1
            }

            jobs.append(job_data_1)




    # 잡플래닛
    url_3 = f"https://www.jobplanet.co.kr/search/job?query={keyword}"
    r_3 = requests.get(url_3, headers=headers_1)

    soup_3 = BeautifulSoup(r_3.text, "html.parser")
    lis_3 = soup_3.find_all("div", class_="w-full overflow-hidden rounded-[12px] border border-gray-100 bg-white")

    for li_3 in lis_3:
        try:
            c_3s = li_3.find("span", class_="jds-h4 truncate text-gray-500")
            c_3 = c_3s.text.strip() if c_3s else "회사명 없음"

            t_3s = li_3.find("h3", class_="jds-h2 break-keep text-gray-900 truncate")
            t_3 = t_3s.text.strip() if t_3s else "제목 없음"

            l_3s = li_3.find("a", class_="flex flex-col items-end px-[20px] pb-[20px] pt-[16px]")
            l_3 = l_3s.get("href") if l_3s else "#"

            d_3 = "기한 미상"
            r_3 = "지역 미상"
            e_3 = "경력 미상"
            spans = li_3.find_all("span", class_="inline-flex items-center gap-[4px]")

            for span in spans:
                text = span.text.replace('·', '').strip()
                if not text:
                    continue
                if 'D-' in text or '~' in text or '상시' in text or '채용' in text:
                    d_3 = text
                elif '년' in text or '경력' in text or '신입' in text or '무관' in text:
                    e_3 = text
                else:
                    r_3 = text

            job_data_3 = {
                "site": "잡플래닛",
                "company": c_3,
                "title": t_3,
                "region": r_3,
                "date": d_3,
                "link": l_3
            }

            jobs.append(job_data_3) 
            
        except Exception as e:
            print(f"잡플래닛 파싱 중 에러: {e}")
            continue
            
    return jobs