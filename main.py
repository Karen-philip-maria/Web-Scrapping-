import requests
from bs4 import BeautifulSoup
import time

def fetch_page(url):
    """Fetch and parse a single page."""
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_articles(soup):
    """Extract all article data from the soup object, ensuring no data is left out."""
    articles = soup.find_all("article", class_="col-sm-6")
    article_data = []

    for index, article in enumerate(articles):
        print(f"Parsing article {index + 1}...") 

        title_tag = article.find("h4", class_="card-title")
        title = title_tag.get_text(strip=True) if title_tag else "No title found"

        content_parts = []
        body = article.find("div", class_="card-body")
        if body:
            for element in body.find_all(["p", "div", "span"], recursive=True):
                text = element.get_text(strip=True)
                if text: 
                    content_parts.append(text)
        content = " ".join(content_parts).strip() if content_parts else "No content found"

        print(f"Title: {title}")  
        print(f"Content: {content[:200]}...") 
        article_data.append({
            'title': title,
            'content': content
        })

    return article_data

def save_articles_to_file(articles, page_number):
    """Save collected articles for a specific page to a file."""
    filename = f"Articles_Page_{page_number}.txt"
    with open(filename, "w", encoding='UTF-8') as f:
        for i, article in enumerate(articles, start=1):
            title = article['title']
            content = article['content']
            f.write(f"Article {i}: \n Title : {title} \n Content : \n{content}\n\n")
            print(f"Page {page_number} - Article {i}: \n Title : {title} \n Content : \n{content}\n")

def scrape_all_pages(base_url):
    """Scrape data from all pages one at a time until no more articles are found."""
    page_number = 1
    while True:
        url = f"{base_url}?page={page_number}"
        print(f"Fetching page {page_number}...")
        soup = fetch_page(url)
        
        if soup is None:
            print(f"Failed to retrieve page {page_number}.")
            break
        
        articles = parse_articles(soup)
        
        if not articles:
            print(f"No more articles found on page {page_number}.")
            break
        
        save_articles_to_file(articles, page_number)
        
        page_number += 1
        time.sleep(1)  
    
    print('All pages have been processed and saved.')

if __name__ == "__main__":
    base_url = "https://ura.go.ug/en/category/imports-exports/customs-enforcements/"
    scrape_all_pages(base_url)








