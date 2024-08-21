import requests
import pdfplumber
import mysql.connector
from io import BytesIO

def fetch_pdf(url):
    """Fetch and read a PDF file from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_text_from_pdf(pdf_file):
    """Extract text from the PDF file."""
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() or ""
    return extracted_text

def parse_text(text):
    """Parse and categorize text extracted from the PDF."""
    extracted_info = []
    lines = text.split('\n')
    for line in lines:
        if 'tariff' in line.lower():  # Adjust this line based on actual content
            extracted_info.append({
                'title': line,
                'content': line
            })
    return extracted_info

def insert_tariffs_to_db(tariffs):
    """Insert tariff information into the database."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',  # Ensure this password is correct
            database='trade_documents'
        )
        cursor = connection.cursor()
        for tariff in tariffs:
            title = tariff['title']
            content = tariff['content']
            cursor.execute(
                "INSERT INTO `tariffs` (`title`, `content`) VALUES (%s, %s)",
                (title, content)
            )
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

def scrape_pdf(url):
    """Fetch, extract, and insert data from a PDF."""
    pdf_file = fetch_pdf(url)
    if pdf_file is None:
        print("Failed to retrieve the PDF file.")
        return
    text = extract_text_from_pdf(pdf_file)
    tariffs = parse_text(text)
    insert_tariffs_to_db(tariffs)
    print('PDF has been processed and data has been inserted into the database.')

if __name__ == "__main__":
    pdf_url = "https://kra.go.ke/images/publications/EAC-CET-2022-VERSION-30TH-JUNE-Fn.pdf"
    scrape_pdf(pdf_url)
