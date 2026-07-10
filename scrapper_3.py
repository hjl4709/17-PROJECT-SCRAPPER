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


    for i in range(page):
        startno = 30 * i 
        url_1 = f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}&startno={startno}"
        
        r_1 = requests.get(url_1, headers=headers_1)
        soup_1 = BeautifulSoup(r_1.text, "html.parser")
        lis_1 = soup_1.find_all("li", class_="c_col")

        for li_1 in lis_1:
            try:
                c_elem = li_1.find("a", class_="cpname")
                c_1 = c_elem.text.strip() if c_elem else "회사명 없음"
                
                t_elem = li_1.find("div", class_="cell_mid")
                if t_elem and t_elem.find("div", class_="cl_top") and t_elem.find("div", class_="cl_top").find("a"):
                    t_1 = t_elem.find("div", class_="cl_top").find("a").text.strip()
                    l_1 = t_elem.find("div", class_="cl_top").find("a").get("href")
                else:
                    t_1 = "제목 없음"
                    l_1 = "#"

                r_elem = li_1.find("div", class_="cl_md")
                span_elems = r_elem.find_all("span") if r_elem else []
                r_1 = span_elems[0].text.strip() if span_elems else "지역 미상"

                d_elem = li_1.find('div', class_="cell_last")
                if d_elem and d_elem.find("div", class_="cl_btm") and d_elem.find("div", class_="cl_btm").find_all("span"):
                    d_1 = d_elem.find("div", class_="cl_btm").find_all("span")[0].text.strip()
                else:
                    d_1 = "마감일 미상"

                job_data_1 = {
                    "company": c_1,
                    "title": t_1,
                    "region": r_1,
                    "date": d_1,
                    "link": l_1
                }
                jobs.append(job_data_1)
                
            except Exception as e:
                print(f"인크루트 파싱 중 에러: {e}")
                continue


    url_3 = f"https://www.jobplanet.co.kr/search/job?query={keyword}"
    r_3 = requests.get(url_3, headers=headers_1)
    
    soup_3 = BeautifulSoup(r_3.text, "html.parser")
    lis_3 = soup_3.find_all("div", class_="w-full overflow-hidden rounded-[12px] border border-gray-100 bg-white")

    for li_3 in lis_3:
        try:
            c_elem = li_3.find("span", class_="jds-h4 truncate text-gray-500")
            c_3 = c_elem.text.strip() if c_elem else "회사명 없음"
            
            t_elem = li_3.find("h3", class_="jds-h2 break-keep text-gray-900 truncate")
            t_3 = t_elem.text.strip() if t_elem else "제목 없음"
            
            l_elem = li_3.find("a", class_="flex flex-col items-end px-[20px] pb-[20px] pt-[16px]")
            l_3 = l_elem.get("href") if l_elem else "#"
            
            span_elems = li_3.find_all("span", class_="inline-flex items-center gap-[4px]")
            if span_elems:
                info_text = span_elems[0].text.strip()
                info_list = info_text.split('·')
                date_3 = info_list[0].strip()
                
                region_3 = "지역 미상"
                experience_3 = "경력 미상"
                
                for item in info_list[1:]:
                    item = item.strip()
                    if '년' in item or '경력' in item or '신입' in item:
                        experience_3 = item
                    else:
                        region_3 = item
            else:
                date_3 = "기한 미상"
                region_3 = "지역 미상"
                experience_3 = "경력 미상"

            job_data_3 = {
                "company": c_3,
                "title": t_3,
                "region": region_3,
                "date": date_3,
                "link": l_3
            }            
            jobs.append(job_data_3) 
            
        except Exception as e:
            print(f"잡플래닛 파싱 중 에러: {e}")
            continue
            
    return jobs