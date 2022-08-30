import requests
import fake_useragent
from bs4 import BeautifulSoup
from datetime import datetime
import asyncio
import aiohttp
import news_db
import time


last_news = []
def get_last_page():
    global last_news
    number_page = 1
    myURL = f'https://www.tesmanian.com'

    ua = fake_useragent.UserAgent()
    headers = {
        "User-Agent": ua.random
    }

    response = requests.get(f'{myURL}/blogs/tesmanian-blog?page={number_page}', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    last_page = soup.find('div', class_="paginate").find_all('a')[2].text
    return int(last_page)


async def get_page_data(session, number_page):
    global last_news
    last_news =[]
    news_db.create_table()

    myURL = f'https://www.tesmanian.com'

    ua = fake_useragent.UserAgent()
    headers = {
        "User-Agent": ua.random
    }
    async with session.get(f'{myURL}/blogs/tesmanian-blog?page={number_page}', headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, 'html.parser')
        resaults = soup.find_all('div', class_="eleven columns "
                                               "omega align_left")

        for resault in resaults:
            title = resault.find('a').text

            date_time_str = resault.find_all('span')[1].text
            date_time_obj = datetime.strptime(date_time_str, '%B %d, %Y')
            date_time = datetime.strftime(date_time_obj, '%Y-%m-%d')

            link = f"{myURL}{resault.find('a').get('href')}"
            last_new_id = news_db.add_news(new_title=title, new_date_time=date_time, new_link=link)
            last_news.append(last_new_id)
        print(f"Page parsing №{number_page} done")


async def gather_data(last_page):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for page in range(1, last_page + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    global last_news
    last_page = get_last_page()
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(gather_data(last_page))
    finally:
        loop.close()


def run(last_page=0):
    global last_news
    if not last_page:
        last_page = get_last_page()
        last_page = last_page
    loop = asyncio.new_event_loop()
    loop.run_until_complete(gather_data(last_page))

if __name__ == '__main__':
    while True:
        main()
        time.sleep(15)

