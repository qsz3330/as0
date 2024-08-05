from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
# from flask import Flask, jsonify
# app = Flask(__name__)


def get_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '100',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '17a0aa66-43c9-4728-82d4-0a65b94285a8',
    }

    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        coins = data['data']

        non_stable_coins = [coin for coin in coins if coin['symbol'] not in ['USDT', 'USDC','FDUSD', 'BUSD', 'DAI']]

        top_liquidity_coins = sorted(non_stable_coins, key=lambda x: x['quote']['USD']['volume_24h'], reverse=True)[:30]

        total_market_cap = sum(coin['quote']['USD']['market_cap'] for coin in top_liquidity_coins)

        weights = {coin['symbol']: coin['quote']['USD']['market_cap'] / total_market_cap for coin in top_liquidity_coins}

        index_value = sum(coin['quote']['USD']['price'] * weight for coin, weight in zip(top_liquidity_coins, weights.values()))

        print(f"The index value based on the top 30 non-stable coins by 24h liquidity is: {round(index_value, 2)}")
        # result = {"message": f"The index value based on the top 30 non-stable coins by 24h liquidity is: {round(index_value, 2)}"}
        # return result
        # return round(index_value, 2)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

# @app.route('/value', methods=['GET'])
# def my_endpoint():
#     result = get_data()
#     return jsonify(result)

if __name__ == "__main__":
    get_data()
    # app.run(host='0.0.0.0', port=80)

