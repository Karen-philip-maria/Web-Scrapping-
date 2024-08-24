# import requests
# from bs4 import BeautifulSoup
# import time
# def fetch_page(url):
#     """Fetch and parse a single page."""
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")
#         return soup
#     except requests.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return None
# def parse_articles(soup):
#     """Extract and categorize articles from the soup object."""
#     categorized_articles = {
#         "Agricultural Documents": [
#             "Certificate of Origin",
#             "Phytosanitary Certificate",
#             "Export License",
#             "Bill of Lading",
#             "Invoice",
#             "Packing List"
#         ],
#         "Electronics": [
#             "Certificate of Conformity",
#             "Export License",
#             "Bill of Lading",
#             "Invoice",
#             "Packing List",
#             "Declaration of Conformity"
#         ],
#         "Clothing": [
#             "Certificate of Origin",
#             "Export License",
#             "Bill of Lading",
#             "Invoice",
#             "Packing List",
#             "Customs Declaration"
#         ],
#         "Textiles and Fabrics": [
#             "Certificate of Origin",
#             "Export License",
#             "Bill of Lading",
#             "Invoice",
#             "Packing List",
#             "Certificate of Authenticity"
#         ]
#     }
#     print("Page source preview:\n", soup.prettify()[:2000])
#     articles = soup.find_all("article", class_="col-sm-6")
#     extracted_info = []
#     for index, article in enumerate(articles):
#         print(f"Parsing article {index + 1}...")
#         title_tag = article.find("h4", class_="card-title")
#         title = title_tag.get_text(strip=True) if title_tag else "No title found"
#         content_parts = []
#         body = article.find("div", class_="card-body")
#         if body:
#             for element in body.find_all(["p", "div", "span"], recursive=True):
#                 text = element.get_text(strip=True)
#                 if text:
#                     content_parts.append(text)
#         content = " ".join(content_parts).strip() if content_parts else "No content found"
#         category = "Other"
#         if any(keyword in title.lower() for keyword in ["agriculture", "farm", "crops"]):
#             category = "Agricultural Documents"
#         elif any(keyword in title.lower() for keyword in ["electronics", "devices"]):
#             category = "Electronics"
#         elif any(keyword in title.lower() for keyword in ["clothing", "apparel"]):
#             category = "Clothing"
#         elif any(keyword in title.lower() for keyword in ["textiles", "fabrics"]):
#             category = "Textiles and Fabrics"
#         extracted_info.append({
#             'title': title,
#             'content': content,
#             'category': category
#         })
#     return extracted_info, categorized_articles
# def display_categorized_info(extracted_info, categorized_articles):
#     """Display categorized articles to the console."""
#     categorized_output = {key: [] for key in categorized_articles.keys()}
#     for info in extracted_info:
#         category = info['category']
#         if category in categorized_articles:
#             categorized_output[category].append({
#                 'title': info['title'],
#                 'content': info['content']
#             })
#     for category, documents in categorized_articles.items():
#         print(f"\n--- {category} ---")
#         print("Required Documents:")
#         for document in documents:
#             print(f" - {document}")
#         print("\nExtracted Articles:")
#         if category in categorized_output:
#             for i, article in enumerate(categorized_output[category], start=1):
#                 title = article['title']
#                 content = article['content']
#                 print(f"\nArticle {i}:")
#                 print(f" Title: {title}")
#                 print(f" Content: {content[:500]}...")
#         else:
#             print("No articles found in this category.")
# def scrape_pages(base_url, num_pages=1):
#     """Scrape data from a limited number of pages and categorize documents."""
#     all_extracted_info = []
#     for page_number in range(1, num_pages + 1):
#         url = f"{base_url}?page={page_number}"
#         print(f"Fetching page {page_number}...")
#         soup = fetch_page(url)
#         if soup is None:
#             print(f"Failed to retrieve page {page_number}.")
#             continue
#         extracted_info, categorized_articles = parse_articles(soup)
#         all_extracted_info.extend(extracted_info)
#         time.sleep(1)
#     display_categorized_info(all_extracted_info, categorized_articles)
#     print('Selected pages have been processed and categorized.')
# if __name__ == "__main__":
#     base_url = "https://ura.go.ug/en/category/imports-exports/customs-enforcements/"
#     scrape_pages(base_url, num_pages=1)



import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "https://www.knbs.or.ke/reports/construction-input-price-index-second-quarter-2024/"

# Send GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Print a snippet of the HTML to understand its structure
    print(soup.prettify()[:1000])  # Print the first 1000 characters of the HTML

    # Adjust the selector based on the actual HTML structure of the page
    articles = soup.find_all("div", class_="article-class")  # Adjust class name based on actual HTML

    # List to store extracted data
    rules = []

    # Open file to write results
    with open("Articles.txt", "w", encoding='UTF-8') as f:
        for i, article in enumerate(articles, start=1):
            # Adjust selectors based on actual HTML structure
            title_tag = article.find("h2")  # Adjust to actual tag if needed
            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            
            body = article.find("div", class_="content-class")  # Adjust class name based on actual HTML
            content = body.get_text(strip=True) if body else "No Content"
            
            # Append to rules list
            rules.append({
                'title': title,
                'content': content
            })
            
            # Write to file
            f.write(f"Article {i}: \nTitle: {title}\nContent: {content}\n\n")
            
            # Print results to console
            print(f"Article {i}: \nTitle: {title}\nContent: {content}\n")
        
    print('Rules extracted:', rules)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

