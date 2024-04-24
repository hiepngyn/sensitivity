import requests
import pantrydb
from bs4 import BeautifulSoup



def access_href(url):
    """
    Takes in a food category and returns all valid
    href urls of items in a given catergory.
    """
    href_list = []
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all(class_="list-group lg-root well")

    for element in elements:
        links = element.find_all('a')
        for link in links:
            href_list.append(link.get("href"))
    return href_list
    
def scrape_food_information(href_list):
    for href in href_list:
        response = requests.get(href)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        product_dict = {}

        elements = soup.find_all(class_="col-xs-12 col-sm-8 col-md-9")
        ingredients = soup.find_all(class_= "col-sm-9 col-md-5 col-lg-6")

        for element, ingredient in zip(elements,ingredients):
            product_name = element.find('h1').get_text(strip=True)   
            product_ingredients = ingredient.get_text(strip=True)
            pantrydb.PANTRY_PUT(product_name,product_ingredients)
            