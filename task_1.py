import aiohttp
import asyncio
from json import loads
from datetime import datetime
from config import BASE_URL, SYMBOL

HOUR_PRICE_URL: str = f'{BASE_URL}/api/v3/ticker?symbol={SYMBOL}&windowSize=1h'


async def check_diff_with_max_price(cur_price: float, max_price: float) -> None:
    """
    В случае, если текущая цена упала ниже максимальной за последний час более чем на 1%, выводит сообщение в консоль.

    :param cur_price: текущая цена
    :type cur_price: float
    :param max_price: максимальная цена за последний час
    :type max_price: float
    :return: None
    """
    if cur_price/max_price < 0.99:
        print(f'{datetime.now()}: текущая цена пары {SYMBOL} упала ниже максимальной за последний час более чем на 1%\n'
              f'Текущая цена: {cur_price}\n'
              f'Максимальная цена за последний час: {max_price}\n')


async def collect_prices() -> None:
    """
    Запрашивает данные о цене пары с сервера Binance.
    Выводит информацию о текущей цене в консоль, а также сравнивает её с максимальной за последний час.

    :return: None
    """
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(5)) as client:
        while True:
            async with client.get(HOUR_PRICE_URL) as response:
                if response.status == 200:
                    result = await response.read()
                    cur_price = float(loads(result)['lastPrice'])
                    max_price = float(loads(result)['highPrice'])
                    await check_diff_with_max_price(cur_price, max_price)
                    print(f'{datetime.now()}: текущая цена: {cur_price}')
                else:
                    print(f'Произошла ошибка при установке соединения с Binance: {response.status}\n'
                          f'Проверьте, что в файле config указан корректный идентификатор пары, '
                          f'или используйте резервный BASE_URL')
                    break


def main():
    asyncio.run(collect_prices())


if __name__ == '__main__':
    main()
