import csv
from scrapper_2 import search_incruit


def save_to_csv(jobs):
    with open ("./downloads.csv", "w", encoding="cp949") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["사이트", "No", "회사", "제목", "지역", "마감일", "상세보기"])
        for i, job in enumerate(jobs):
            csv_writer.writerow([job["site"], i+1, job["company"], job["title"], job["region"], job["date"], job["link"]])