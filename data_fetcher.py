import asyncio

import aiohttp
from flask import jsonify

from configs import social_media_endpoints


class Singleton(object):
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
        return class_._instances[class_]


class DataFetcher(Singleton):
    async def fetch_data(self, session, url):
        async with session.get(url) as response:
            try:
                data = await response.json()
                return data
            except Exception as e:
                print(f"Error fetching data from {url}: {str(e)}")
                return {}

    async def get_social_network_activity(self):

        json_response = {}

        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_data(session, url) for url in social_media_endpoints]
            results = await asyncio.gather(*tasks)

        for url, result in zip(social_media_endpoints, results):
            platform_name = url.split("/")[-1]
            json_response[platform_name] = len(result)

        return jsonify(json_response)
