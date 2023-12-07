import asyncio
from flask import Flask, jsonify
import aiohttp

app = Flask(__name__)

async def fetch_data(session, url):
    async with session.get(url) as response:
        try:
            data = await response.json()
            return data
        except Exception as e:
            # Handle JSON decoding errors or other exceptions
            print(f"Error fetching data from {url}: {str(e)}")
            return {}

async def social_network_activity():
    social_media_endpoints = [
        "https://takehome.io/twitter",
        "https://takehome.io/facebook",
        "https://takehome.io/instagram"
    ]

    json_response = {}

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in social_media_endpoints]
        results = await asyncio.gather(*tasks)

    # Populate the json_response dictionary with the obtained data
    for url, result in zip(social_media_endpoints, results):
        platform_name = url.split("/")[-1]
        print(url)
        print("\n")
        print(result)
        print("\n")
        print(platform_name)
        print("\n")
        json_response[platform_name] = len(result)

    return jsonify(json_response)

# Define the route for the endpoint
@app.route("/")
def index():
    # Run the asynchronous function in the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(social_network_activity())
    return result

if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)


    app.run(debug=True)