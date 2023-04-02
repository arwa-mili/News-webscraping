# importing the necessary packages
import uvicorn as uvicorn
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class NewsModel:
    def __init__(self, title, desc, link, date):
        self.title = title,
        self.desc = desc,
        self.link = link,
        self.date=date


@app.get("/news")
def get_news():
    found_href = False
    url = "https://spectrum.ieee.org/topic/artificial-intelligence/"
    response = requests.get(url)
    news = []
    soup = BeautifulSoup(response.content, "html.parser")
    divs = soup.find_all("div", {"class": "posts-wrapper clearfix"})



    div2 = soup.find_all("div", {"data-category": "Artificial Intelligence"})
    for d in div2:
        article = NewsModel(None, None, None, None)
        links = d.find_all("a")
        for link in links:
            href = link.get("href")

            if "topic" not in href and "type" not in href and "magazine" not in href:
                if href:
                    if not found_href:
                        article.link = href
                        found_href = True
                        break
            found_href = False

        h2_tags = d.find_all("h2")

        for h2 in h2_tags:
            title = h2.text
            article.title = title

        h3_tags = d.find_all("h3")
        for h3 in h3_tags:
            description = h3.text
            article.desc = description

        dates = d.find("div", class_="social-date")
        date = dates.find_all("span")
        for dt in date:
            daate = dt.text
            article.date = daate

        news.append(article)

    return {"news": news}

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)