import re
import requests
from decimal import Decimal
from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5',
}


def fetch_page(url: str):
    """Fetches page and returns content of BeautifulSoup object"""
    res = requests.get(url, headers=HEADERS)   
    page = BeautifulSoup(res.content, "lxml")
    return page


def get_price(soup, path):
    """Finds price in content of BeautifulSoup object

    Args:
        soup: content of BeautifulSoup object
        path: object with tag and id, class or attrs of the HTML element where price is located.
            child property can be added for nested tags (as many as needed)
            example: {
                'tag': 'div',
                'class': 'price-container',
                'child': {
                    'tag': 'span',
                    'id': 'product-price',
                }
            }
    
    Returns:
        price: decimal object
    """
    result = None
    tag = path.get('tag')

    if path.get('attrs', False):
        result = soup.find(tag, attrs=path.get('attrs'))

    elif path.get('id', False):
        id = path.get('id')
        result = soup.find(tag, id=id)

    elif path.get('class', False):
        class_ = path.get('class', False)
        result = soup.find(tag, class_=class_)
    
    if path.get('child', False):
        return get_price(result, path.get('child'))
    
    # Clean price string
    price = result.string.strip()
    
    pattern = re.compile(r'(?![\.\,])[\D]+')
    result = pattern.sub('', price)

    return Decimal(result)