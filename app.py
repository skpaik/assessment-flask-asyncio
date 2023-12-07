import asyncio

from flask import Flask

from data_fetcher import DataFetcher

app = Flask(__name__)

data_fetcher = DataFetcher()


@app.route("/")
def social_network_activity():
    # Run the asynchronous function in the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(data_fetcher.get_social_network_activity())
    return result


if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)

    app.run(debug=True)
