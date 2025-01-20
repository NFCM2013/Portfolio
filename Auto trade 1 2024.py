import requests
import pandas as pd
import time

class TradingBot:
    def __init__(self, api_key, username, password, account_id):
        self.base_url = "任意"
        self.api_key = api_key
        self.username = username
        self.password = password
        self.account_id = account_id
        self.headers = {"任意": self.api_key, "Content-Type": "application/json"}
        self.session = requests.Session()
        self.authenticate()

    def authenticate(self):
        auth_url = f"{self.base_url}/session"
        auth_data = {
            "identifier": self.username,
            "password": self.password
        }
        response = self.session.post(auth_url, json=auth_data, headers=self.headers)
        if response.status_code == 200:
            cst = response.headers["CST"]
            x_sec_token = response.headers["任意"]
            self.headers.update({"CST": cst, "任意": x_sec_token})
            print("認証成功!")
        else:
            raise Exception(f"認証失敗: {response.json()}")

    def get_market_price(self, epic):
        url = f"{self.base_url}/markets/{epic}"
        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            market_data = response.json()
            bid = market_data["snapshot"]["bid"]
            offer = market_data["snapshot"]["offer"]
            return {"bid": bid, "offer": offer}
        else:
            raise Exception(f"市場データ取得失敗: {response.json()}")

    def place_order(self, epic, direction, size, order_type="MARKET"):
        url = f"{self.base_url}/positions/otc"
        order_data = {
            "epic": epic,
            "direction": direction,  # "BUY" または "SELL"
            "size": size,
            "orderType": order_type,
            "currencyCode": "USD",
            "forceOpen": True,
            "expiry": "-",
        }
        response = self.session.post(url, json=order_data, headers=self.headers)
        if response.status_code == 200:
            print(f"注文成功: {response.json()}")
            return response.json()
        else:
            raise Exception(f"注文失敗: {response.json()}")

    def run(self, epic, size, profit_target=0.01):
        while True:
            try:
                prices = self.get_market_price(epic)
                print(f"現在価格: Bid={prices['bid']}, Offer={prices['offer']}")

                if prices["bid"] < 任意:
                    print("買い注文を送信...")
                    self.place_order(epic, "BUY", size)

                elif prices["bid"] > 任意:
                    print("売り注文を送信...")
                    self.place_order(epic, "SELL", size)

                time.sleep(30)
            except Exception as e:
                print(f"エラー: {e}")
                time.sleep(10)


