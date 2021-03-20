import requests
from bs4 import BeautifulSoup
import time
from multiprocessing import Process, Manager
import sys
from datetime import datetime


"""
This code down below goes to a Wikipedia Category page, it iterates
through the links from 'A' till 'Я' of the russian alphabet and counts how many 
animals start with a specific letter. 
"""


def connection():
    url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    try:
        page = requests.get(url).text
    except:
        sys.stdout.write('\b' * 16)  # cleans 'Please, wait...' message from the screen
        print('Something went wrong. Please, check your connection and try again.')
        return
    return page


# Function that grabs all of the necessary links from a page
def list_of_urls(page):
    soup = BeautifulSoup(page, 'html.parser')
    if not soup:
        return
    try:
        urls = soup.find('div', id='mw-pages').find_all('a')
    except AttributeError:
        sys.stdout.write('\b' * 16)
        print('Link that you\'ve provided is incorrect.')
        return
    return urls


# Function that specifically gets the url to the next page and list of urls that represents animals
def new_url_and_animals(urls):
    if urls:
        url = 'https://ru.wikipedia.org/' + urls[-1].get('href')
        return url, urls


def main(dictionary):
    page = connection()
    if not page:
        return
    elif not new_url_and_animals(list_of_urls(page)):
        return
    while True:
        url, animals = new_url_and_animals(list_of_urls(page))
        for animal in animals:
            if animal.text[0] == 'A':
                return dictionary  # condition is to stop when we get to the english alphabet
            else:
                if animal.text != 'Предыдущая страница' and animal.text != 'Следующая страница':
                    if animal.text[0] in dictionary.keys():  # condition to avoid wiki bugs like english first letters
                        dictionary[animal.text[0]] += 1
        page = requests.get(url).text


def printing_dictionary(d: dict):
    sys.stdout.write('\b' * 17)
    for key, value in d.items():
        print(f'{key}: {value}')


# Function that represents loading process while main main function is running
def progress_line():
    for counter in range(4):
        if counter == 4 or counter == 0:
            sys.stdout.write('Please, wait')
        time.sleep(0.3)
        sys.stdout.write('.')
        counter += 1
        if counter == 4:
            sys.stdout.write('\b' * 16)


if __name__ == '__main__':
    start = datetime.now()
    manager = Manager()
    dictionary = manager.dict({a: 0 for a in [chr(ord("А") + m) for m in range(32)]})
    process = Process(target=main, args=(dictionary, ))
    process.start()
    while process.is_alive():
        progress_line()
    if any(dictionary.values()):  # to avoid printing an empty dict if something went wrong.
        printing_dictionary(dictionary)
    end = datetime.now()
    print("Time is equal: ", end - start)
