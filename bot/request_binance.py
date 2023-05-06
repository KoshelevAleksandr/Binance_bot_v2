import datetime
import requests

base_url = 'https://api.binance.com'
trade_price_url = 'https://testnet.binancefuture.com/fapi/v1/trades?symbol=BTCUSDT&limit=1'
reserve_url_btc = 'https://testnet.binancefuture.com/fapi/v1/ticker/price?symbol=BTCUSDT'


def btc_in_usdt():
    btc_usdt = requests.get(trade_price_url).json()[0]
    time_btc = datetime.datetime.fromtimestamp(btc_usdt['time'] / 1000.0)
    reserve_btc_usdt = requests.get(reserve_url_btc).json()
    reserve_time_btc = datetime.datetime.fromtimestamp(reserve_btc_usdt['time'] / 1000.0)

    if (datetime.datetime.now() - time_btc).seconds > 60:
        if reserve_time_btc > time_btc:
            price_usdt = float(reserve_btc_usdt['price'])
        else:
            price_usdt = float(btc_usdt['price'])
    else:
        price_usdt = float(btc_usdt['price'])

    return price_usdt


def usdt_in_eur():
    eur_usdt = requests.get('https://api.binance.com/api/v3/depth?symbol=EURUSDT&limit=1').json()
    usdt_eur = 1 / ((float(eur_usdt['bids'][0][0]) + float(eur_usdt['asks'][0][0])) / 2)
    return usdt_eur


def usdt_in_rub():
    usdt_rub = requests.get('https://api.binance.com/api/v3/depth?symbol=USDTRUB&limit=1').json()
    price = (float(usdt_rub['bids'][0][0]) + float(usdt_rub['asks'][0][0])) / 2
    return price


def currency_selection(currency):
    if currency == 'usdt':
        price = round(btc_in_usdt(), 2)
        return price

    elif currency == 'eur':
        btc_usdt = btc_in_usdt()
        usdt_eur = usdt_in_eur()
        price = round((btc_usdt * usdt_eur), 2)
        return price

    elif currency == 'rub':
        btc_usdt = btc_in_usdt()
        usdt_rub = usdt_in_rub()
        price = round((btc_usdt * usdt_rub), 2)
        return price
