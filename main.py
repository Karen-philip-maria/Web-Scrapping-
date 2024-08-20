       
import requests
from bs4 import BeautifulSoup
response = requests.get("https://ura.go.ug/en/category/imports-exports/customs-enforcements/")
soup = BeautifulSoup(response.text, "html.parser")
articles = soup.find_all("article", class_="col-sm-6")
# print('article ===>', articles)
rules = []
with open("Articles.txt", "w", encoding='UTF-8') as f:
    for i, article in enumerate(articles, start=1):
        title_tag = article.find("h4", class_="card-title")
        if title_tag:
            title = title_tag.get_text(strip=True)
        body = article.find("div", class_="card-body")
        if body:
            content = body.get_text(strip=True)
        rules.append({
            'title':title,
            'content':content
        })
        f.writelines(f"Article {i}: \n Title : {title} \n  \t{content} \n")
        print(f"Article {i}: \n Title : {title} \n  \t{content}")
        print("\n")
print('rules ====>', rules)