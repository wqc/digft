from fcoin3 import Fcoin
import time
import sys

UsdtMin = 38000
Amount = 100

fcoin = Fcoin()
fcoin.auth('', '')

def getUsdt():
    balance = fcoin.get_balance()
    data = balance['data']
    for item in data:
        if item['currency'] == 'usdt':
            return float(item['balance'])
    return 0

def getAvaiCoin(token):
    balance = fcoin.get_balance()
    data = balance['data']
    for item in data:
        if item['currency'] == token:
            return float(item['available'])
    return 0

def getAvaiUsdt():
    return getAvaiCoin('usdt')

def getAvaiFt():
    return getAvaiCoin('ft')

def getPendingNumber():
    orders = fcoin.list_orders(symbol='ftusdt', states='submitted')
    pendingNum = len(orders['data'])
    return pendingNum

def cancelMaximalSellOrder():
    orders = fcoin.list_orders(symbol='ftusdt', states='submitted')
    if orders['status'] == 0:
        print('status ok !')
        if len(orders['data']) <= 0 :
            return False

        maxi_price = -1
        maxi_id = 0
        for order in orders['data']:
            if order['side'] == 'sell' :
                price = float(order['price'])
                if maxi_price < 0 or maxi_price < price :
                    maxi_price = price
                    maxi_id = order['id']
        if maxi_price < 0 :
            return False

        print('maxi_price -> ', maxi_price, 'maxi_id -> ', maxi_id)
        print(fcoin.cancel_order(maxi_id))
    return True

def cancelMinimumBuyOrder():
    orders = fcoin.list_orders(symbol='ftusdt', states='submitted')
    if orders['status'] == 0:
        print('status ok !')
        if len(orders['data']) <= 0 :
            return False

        mini_price = -1
        mini_id = 0
        for order in orders['data']:
            if order['side'] == 'buy' :
                price = float(order['price'])
                if mini_price < 0 or mini_price > price :
                    mini_price = price
                    mini_id = order['id']
        if mini_price < 0:
            return False

        print('mini_price -> ', mini_price, 'mini_id -> ', mini_id)
        print(fcoin.cancel_order(mini_id))
    return True

def dealOrder():
    try:
        existNumber = getPendingNumber()
        avaiUsdt = getAvaiUsdt()
        avaiFt = getAvaiFt()
    except Exception as e:
        return

    print('existNumber -> ', existNumber)
    print('avaiUsdt -> ', avaiUsdt)
    time.sleep(0.2)

    ticker = fcoin.get_market_ticker("ftusdt")
    lastPrice = ticker["data"]["ticker"][0]
    print("lastPrice -> ", lastPrice)

    buy_price = lastPrice

    consumeUst = Amount * buy_price
    if avaiUsdt - consumeUst  >= UsdtMin:
        print('usdt enough!')
    else:
        print('usdt not enough, go to cancel minimum order')
        try:
            res = cancelMinimumBuyOrder()
            if res :
                time.sleep(0.2)
                return
            else:
                print('no order canceled , just go on to sell !')
        except Exception as e:
            print(e)
            print('fail to cancel minimum order, just go on')

    if avaiFt < Amount:
        print('ft not enough, go to cancel maximal sell order')
        try:
            cancelSellRes = cancelMaximalSellOrder()
            if cancelSellRes:
                time.sleep(0.2)
                return
            else:
                print('no order canceled, just go go to buy !')
        except Exception as e:
            print('fail to cancel maximal sell order, jus go on')
    else:
        print('ft engough')

    fcoin.sell('ftusdt',buy_price, Amount)
    fcoin.buy('ftusdt', buy_price, Amount)

    cnt = 0
    while True:
        time.sleep(1)
        try:
            pendingNum = getPendingNumber() - existNumber
        except Exception as e:
            print(e);
            time.sleep(2)
            continue

        if pendingNum <= 0:
            print('all dealed !')
            break
        else :
            cnt += 1
            print("pending times -> ", cnt)
            if cnt > 10 :
                print('time out, break to next!')
                break


if __name__ == "__main__":
    while True:
        dealOrder()
        time.sleep(2)
        sys.stdout.flush()
