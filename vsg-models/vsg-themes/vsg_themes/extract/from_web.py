import logging

import aiohttp
import json
import re
import asyncio
from bs4 import BeautifulSoup

from vsg_utils.fs import check_dir_exists_create_if_not


def clean_content(content):
    pattern = re.compile(r'<a\b[^>]*>(.*?)</a>')

    content = pattern.sub(r'\1', content)

    # Remove other irrelevant data (e.g., HTML tags, scripts, etc.) using BeautifulSoup
    soup = BeautifulSoup(content, 'html5lib')
    for script in soup(['script', 'style']):
        script.extract()

    data = soup.get_text().strip()

    return data


async def get_data_from_url_as_json(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                await asyncio.sleep(2)
                data = await response.text()
            else:
                logging.warning(f"Response code: {response.status}")
                data = []

    return data


async def get_data_from_url_and_save_to_file(url, output_file):
    try:
        data = await get_data_from_url_as_json(url)

        data = clean_content(data)

        # Convert the cleaned webpage content to JSON format
        json_content = {
            "url": url,
            "content": data
        }
        # Save the JSON content to a file
        with open(output_file, 'w') as file:
            json.dump(json_content, file, indent=4)

        print(f"Page content saved as {output_file}")

    except aiohttp.ClientError as err:
        print(f"An error occurred: {err}")


def get_data_from_url(url, output_file):

    check_dir_exists_create_if_not(output_file)

    asyncio.run(
        get_data_from_url_and_save_to_file(
            url,
            output_file
        )
    )
