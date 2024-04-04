import aiohttp
import json
import re
import asyncio
from bs4 import BeautifulSoup


def clean_content(content):
    # Remove links (URLs)
    content = re.sub(r'http\S+|www.\S+', '', content, flags=re.MULTILINE)

    # Remove other irrelevant data (e.g., HTML tags, scripts, etc.) using BeautifulSoup
    soup = BeautifulSoup(content, 'html5lib')
    for script in soup(['script', 'style']):
        script.extract()

    return soup.get_text().strip()


async def get_data_from_url_as_json(url: str):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
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
    asyncio.run(
        get_data_from_url_and_save_to_file(
            url,
            output_file
        )
    )


def load_json_data(output_file: str) -> dict:
    data = dict()

    try:
        with open(output_file) as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"File {output_file} not found.")

    except json.JSONDecodeError:
        print(f"Error decoding JSON from {output_file}.")

    return data
