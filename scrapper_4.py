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
    for i in range(page):   
        jp_page = i 
        url_3 = f"https://www.jobplanet.co.kr/api/v3/search/postings?query={keyword}&page={jp_page}&page_size=9"
        
        try:
            r_3 = requests.get(url_3, headers=headers_1, timeout=10)
            if r_3.status_code != 200:
                print(f"[경고] 잡플래닛 서버가 접속을 차단했습니다. 상태 코드: {r_3.status_code}")
                break
            api_data = r_3.json()
            
        except Exception as e:
            print(f"[치명적 에러] 잡플래닛 요청 실패: {e}")
            break

        items = api_data.get("data", {}).get("items", [])[:2]
        
        if not items:
            break

        for item in items:
            try:
                c_3 = item.get("company", {}).get("name", "회사명 없음")
                t_3 = item.get("title", "제목 없음")
                
                cities = item.get("cities", [])
                region_3 = cities[0] if cities else "지역 미상"
                
                date_3 = item.get("deadline_message") or item.get("end_at") or "기한 미상"
                
                job_id = item.get("id", "")
                l_3 = f"https://www.jobplanet.co.kr/job/search?posting_ids={job_id}"
                
                job_data_3 = {
                    "site": "잡플래닛",
                    "company": c_3,
                    "title": t_3,
                    "region": region_3,
                    "date": date_3,
                    "link": l_3
                }
                jobs.append(job_data_3)
                
            except Exception as e:
                print(f"잡플래닛 API 파싱 중 에러: {e}")
                continue
            
    return jobs