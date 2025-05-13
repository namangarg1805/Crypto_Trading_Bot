import time
import requests
from cryptography.hazmat.primitives.asymmetric import ed25519
from urllib.parse import urlparse, urlencode
import urllib
import os
# Takinng secret key and api key from the user as input
secret_key = input("Enter your secret key: ")
api_key = input("Enter your api key: ")
os.environ['secret_key'] = secret_key
os.environ['api_key'] = api_key
base_url = "https://coinswitch.co"
epoch_time = str(int(time.time() * 1000))
print(secret_key)
payload={}

endpoint = "/trade/api/v2/time"

url = base_url + endpoint

headers = {
  'Content-Type': 'application/json',
}
response = requests.request("GET", url, headers=headers, json=payload)

server_time = response.json()["serverTime"]
print(server_time)
def get_signature(method, endpoint, params, epoch_time):
    unquote_endpoint = endpoint
    if method == "GET" and len(params) != 0:
        endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
        unquote_endpoint = urllib.parse.unquote_plus(endpoint)
    signature_msg = method + unquote_endpoint + epoch_time
    request_string = bytes(signature_msg, 'utf-8')
    secret_key_bytes = bytes.fromhex(os.environ.get("secret_key"))
    secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
    signature_bytes = secret_key.sign(request_string)
    signature = signature_bytes.hex()
    return signature

# You can validate the keys provided by Coinswitch using the URL given below:
method = "GET"
endpoint = "/trade/api/v2/validate/keys"
params = {}

signature=get_signature(method,endpoint,params,epoch_time)

url = base_url + endpoint

payload={}

headers = {
  'Content-Type': 'application/json',
  'X-AUTH-SIGNATURE': signature,
  'X-AUTH-APIKEY': api_key,
  'X-AUTH-EPOCH': epoch_time
}

response = requests.request(method, url, headers=headers, json=payload)
print(response.json()["message"])

# Use the code below to check if your ecosystem has been successfully connected to the CoinSwitch ecosystem.
method="GET"
endpoint = "/trade/api/v2/ping"
params = {}

signature = get_signature(method,endpoint,params,epoch_time)

headers = {
  'Content-Type': 'application/json',
  'X-AUTH-SIGNATURE': signature,
  'X-AUTH-APIKEY': api_key,
  'X-AUTH-EPOCH': epoch_time
}

payload = {}

url = base_url+endpoint

response = requests.request(method, url, headers=headers, json=payload)
print(response.json()["message"])

# Use the following endpoint to check trading info:
method="GET"
endpoint = "/trade/api/v2/tradeInfo"
params = {
  "exchange": "coinswitchx",
  "symbol": "BRETT/INR"
}

signature = get_signature(method,endpoint,params,epoch_time)
headers = {
  'Content-Type': 'application/json',
  'X-AUTH-SIGNATURE': signature,
  'X-AUTH-APIKEY': api_key,
  'X-AUTH-EPOCH': epoch_time
}

url = base_url + endpoint

response = requests.request(method, url, headers=headers, params=params)
response.json()["data"]

# Use the following endpoint to get the 24hr ticker for specific coin:
def get_24hr_data(symbol):
    method = "GET"
    params = {
    "symbol": symbol,
    "exchange": "coinswitchx"
    }

    endpoint = "/trade/api/v2/24hr/ticker"

    signature = get_signature(method,endpoint,params,epoch_time)

    endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)

    headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': api_key,
    'X-AUTH-EPOCH': epoch_time
    }
    url = base_url + endpoint

    payload = {}

    response = requests.request(method, url, headers=headers, json=payload)
    coin_data = response.json()["data"]["coinswitchx"]
    for key, value in coin_data.items():
        try:
            coin_data[key] = float(value)
        except (ValueError, TypeError):
            # print(f"Warning: Could not convert value for key {key} to integer. Keeping original value.")
            coin_data[key] = value  # Keep original value if conversion fails
    return coin_data

def buy_coin(symbol,ltp,qty):
    # Use the following endpoint to place a new order on the exchange:
    # CAUTIOUS WHILE RUNNING THIS CODE AS IT WILL DEDUCT MONEY FROM WALLET AND CAN SELL ALSO

    method = "POST"
    endpoint = "/trade/api/v2/order"

    signature = get_signature(method,endpoint,params,epoch_time)

    headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': api_key,
    'X-AUTH-EPOCH': epoch_time
    }

    url = base_url + endpoint

    payload = {
    "side":"buy",
    "symbol":symbol,
    "type":"limit",
    "price":ltp,
    "quantity":qty,
    "exchange":"coinswitchx"
    }
    response = requests.request(method, url, headers=headers, json=payload)
    return response

def sell_coin(symbol,ltp,qty):
    # Use the following endpoint to place a new order on the exchange:
    # CAUTIOUS WHILE RUNNING THIS CODE AS IT WILL DEDUCT MONEY FROM WALLET AND CAN SELL ALSO
    method = "POST"
    endpoint = "/trade/api/v2/order"

    signature = get_signature(method,endpoint,params,epoch_time)

    headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': api_key,
    'X-AUTH-EPOCH': epoch_time
    }
    url = base_url + endpoint

    payload = {
    "side":"sell",
    "symbol":symbol,
    "type":"limit",
    "price":ltp,
    "quantity":qty,
    "exchange":"coinswitchx"
    }
    response = requests.request(method, url, headers=headers, json=payload)
    return response

def portfolio_balance():
    payload={}
    params={}
    method = "GET"
    endpoint = "/trade/api/v2/user/portfolio"
    signature = get_signature(method,endpoint,params,epoch_time)
    headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': api_key,
    'X-AUTH-EPOCH': epoch_time
    }
    url = "https://coinswitch.co/trade/api/v2/user/portfolio"
    response = requests.request(method, url, headers=headers, json=payload)
    new_data = []
    data = response.json()["data"]
    for item in data:
        if isinstance(item, dict):
            new_item = {}
            for key, value in item.items():
                if isinstance(value, (int, float, str)): #check for string
                    try:
                        new_item[key] = float(value)
                    except ValueError:
                         new_item[key] = value #if string is not convertible, keep original
                else:
                    new_item[key] = value
            new_data.append(new_item)
        else:
            new_data.append(item) #if item is not a dict, append as is
    return new_data

def open_orders():
    method="GET"
    params = {
        "exchanges":"coinswitchx",
        "open": True
    }

    payload = {}

    endpoint = "/trade/api/v2/orders"

    signature = get_signature(method,endpoint,params,epoch_time)

    endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)

    url = "https://coinswitch.co" + endpoint

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-SIGNATURE': signature,
        'X-AUTH-APIKEY': api_key,
        'X-AUTH-EPOCH': epoch_time
    }

    response = requests.request("GET", url, headers=headers,json=payload)
    return response

def coin_balance_check(symbol):
    res = portfolio_balance()
    for i in res:
        if i["currency"]==symbol:
            return i
        else:
            pass
    return 0

# prev_minima=min(coin_past_data[-5:-1])
# coin_past_data[-5:]
cnt=0
prev_minima=100
coin_past_data =  [5.53, 5.49, 5.48, 5.58, 5.57, 5.57, 5.57, 5.57, 5.53, 5.53, 5.67, 5.63, 5.63, 5.65, 5.65, 5.65, 5.7, 5.7]
def buy_decision():
    global prev_minima
    brett_data = get_24hr_data("BRETT/INR")
    brett_balance = coin_balance_check("BRETT")
    coin_past_data.append(brett_data["lastPrice"])
    res =  open_orders()
    res = res.json()["data"]["orders"]
    mins_before = 60
    t = int((mins_before/15)*-1)
    print("coin ltp",coin_past_data[-1])
    print("Minima: ",prev_minima)
    if len(res)==0:
        # print("1x")
        if brett_data["percentageChange"]<0:
            # print("2x")
            if coin_past_data[-1]>coin_past_data[-2]:
                # print("3x")
                new_minima=coin_past_data[-2]
                if new_minima<prev_minima:
                    # print("4x")
                    prev_minima=new_minima
                    if coin_past_data[-1]>coin_past_data[-3] and coin_past_data[-1]>coin_past_data[t]:
                        # print("dx")
                        decision = 1
                    else:
                        decision=0
                else:
                    decision =0
            else:
                decision=0
        else:
            prev_minima=100
            decision=0
    else:
        decision = 0
    return decision

def sell_decision():
    brett_data = get_24hr_data("BRETT/INR")
    brett_balance = coin_balance_check("BRETT")
    if brett_balance!=0:
        my_price = brett_balance["buy_average_price"]+(3*brett_balance["buy_average_price"])/100
        if brett_data["percentageChange"]>0 and brett_balance["current_value"]>150 and brett_data["lastPrice"]>my_price:
            decision = 1
        else:
            decision = 0
    else:
        decision = 0
    return decision

def buy_loop():
    while True:
        global cnt
        cnt+=1
        print("Buy loop running: ",cnt)
        coin_data = get_24hr_data("BRETT/INR")
        decision = buy_decision()
        print("buy decision taken: ",decision)
        if decision==1:
            ltp = coin_data["lastPrice"]+(1*coin_data["lastPrice"])/100
            symbol = "BRETT/INR"
            qty=160/ltp
            res = buy_coin(symbol,ltp=ltp,qty=qty)
            if res.status_code==200:
                print("Bought")
            else:
                print("Error")
        time.sleep(900) #loop will run 100 times in 24hr

def sell_loop():
    while True:
        print("sell loop running")
        coin_data = get_24hr_data("BRETT/INR")
        decision = sell_decision()
        brett_balance = coin_balance_check("BRETT")
        print("sell decision taken: ",decision)
        if decision==1:
            ltp = coin_data["lastPrice"]-(coin_data["lastPrice"]/100)
            symbol = "BRETT/INR"
            qty=brett_balance["main_balance"]
            res = sell_coin(symbol,ltp=ltp,qty=qty)
            if res.status_code==200:
                print("Sold")
            else:
                print("Error")
        time.sleep(900) #loop will run 100 times in 24hr

import threading
import time
from concurrent.futures import ThreadPoolExecutor
def main():
    """
    Runs the two loops concurrently using ThreadPoolExecutor, which is
    well-suited for Colab.  It avoids potential issues with thread
    management in that environment.
    """
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(buy_loop)
        executor.submit(sell_loop)
    print("Both loops have finished.")

if __name__ == "__main__":
    main()

print(coin_past_data)
print(prev_minima)

