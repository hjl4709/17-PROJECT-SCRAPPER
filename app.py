from flask import Flask, render_template, request, send_file, redirect
from scrapper_4 import search_incruit
from file import save_to_csv

app = Flask(__name__)

db = {}


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/search')

def search():
    keyword = request.args.get("keyword")
    page = int(request.args.get("page", 1))

    if keyword == "":
        return redirect("/")
    
    cache_key = f"{keyword}_{page}"
    
    if cache_key in db:
        jobs = db[cache_key]
    else:
        jobs = search_incruit(keyword, page)
        db[cache_key] = jobs
   
    return render_template("search.html", jobs=enumerate(jobs), keyword=keyword, count=len(jobs), page=page)       # jobs = jobs 첫번째 jobs는 search.html로 보내는 역할 


@app.route("/file")
def file():
    keyword = request.args.get("keyword")
    page = int(request.args.get("page", 1))

    if keyword == "":
        return redirect("/")
    
    cache_key = f"{keyword}_{page}"
    
    if cache_key in db:
        jobs = db[cache_key]
    else:
        jobs = search_incruit(keyword, page)
        db[cache_key] = jobs
        
    save_to_csv(jobs)
    return send_file("./downloads.csv", as_attachment=True)
        
    save_to_csv(jobs)
    return send_file("./downloads.csv", as_attachment=True)




# @app.route('/hello')            # 인터넷 경로 -> 적힌 주소로 가게되면 밑의 함수가 실행됨.
# def hello():
#     return "안녕하세요."



if __name__ == '__main__':
    app.run()