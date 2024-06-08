from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

from bs4 import BeautifulSoup

app = FastAPI()

class BookInfo(BaseModel):
    title: str
    author: str
    imprint: str
    place_of_publication: str
    description: str
    permalink: str
    isbn: str
    # subject: list[str]
    added_entry: str
    udc: str
    
    
def extract_book_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    book_details = {}

    # Extracting Title, Author, Imprint, Place of Publication, and Description
    title = soup.find('td', class_='bibInfoLabel', text='Title').find_next_sibling('td').text.strip()
    author = soup.find('td', class_='bibInfoLabel', text='Author').find_next_sibling('td').text.strip()
    imprint = soup.find('td', class_='bibInfoLabel', text='Imprint').find_next_sibling('td').text.strip()
    place_of_publication = soup.find('td', class_='bibInfoLabel', text='Place of publ.').find_next_sibling('td').text.strip()
    description = soup.find('td', class_='bibInfoLabel', text='Description').find_next_sibling('td').text.strip()

    book_details['title'] = title
    book_details['author'] = author
    book_details['imprint'] = imprint
    book_details['place_of_publication'] = place_of_publication
    book_details['description'] = description

    # Extracting additional information
    permalink = soup.find('td', class_='bibInfoData', id='permalink').text.strip()
    isbn = soup.find('td', class_='bibInfoLabel', text='ISBN').find_next_sibling('td').text.strip()
    # subject = [s.strip() for s in soup.find('td', class_='bibInfoLabel', text='Subject').find_next_sibling('td').stripped_strings]
    added_entry = soup.find('td', class_='bibInfoLabel', text='Added entry').find_next_sibling('td').text.strip()
    udc = soup.find('td', class_='bibInfoLabel', text='UDC').find_next_sibling('td').text.strip()

    book_details['permalink'] = permalink
    book_details['isbn'] = isbn
    # book_details['subject'] = subject
    book_details['added_entry'] = added_entry
    book_details['udc'] = udc

    return BookInfo(**book_details)
    
@app.get("/parse", response_model=BookInfo)
async def parse_html(isbn: str):
    try:
        url = f"https://www.ester.ee/search/i?searchtype=i&searcharg={isbn}"
        
        # Fetch the HTML content of the page
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        res = extract_book_info(response.text)
        # print(res)
        
        return res
        # Return the extracted data as JSON
        # return BookInfo(
        #     title=title,
        #     author=author,
        #     imprint=imprint,
        #     place_of_publication=place_of_publication,
        #     description=description,
        #     permalink=permalink,
        #     isbn=isbn,
        #     subject=subjects,
        #     added_entry=added_entry,
        #     udc=udc
        # )
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing HTML: {str(e)}")