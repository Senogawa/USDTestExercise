import aiohttp
import asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

async def get_usd_course() -> str:
    """
    Возвращает текущий курс доллара на бирже
    """

    url = "https://www.profinance.ru/currency_usd.asp"
    headers = {
        "user-agent": UserAgent().random
    }

    async with aiohttp.ClientSession(headers = headers) as session:
        async with session.get(url = url) as res:
            if res.status != 200:
                raise aiohttp.ClientConnectionError(f"status code: {res.status}")
            
            html = await res.text()

    soup = BeautifulSoup(html, "lxml")
    tds = soup.find_all(
        "td",
        attrs = {
            "class": "cell"
        }
    )

    return tds[-1].b.text



if __name__ == "__main__":
    res = asyncio.run(get_usd_course())
    print(res)