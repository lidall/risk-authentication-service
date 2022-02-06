import asyncio
import aiohttp


async def main():
    url = 'http://192.168.0.109:8080/log'
    with open('data.txt', 'rb') as f:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={'key': f}) as response:
                return await response.text()


text = asyncio.run(main())  # Assuming you're using python 3.7+
print(text)
