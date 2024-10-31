import requests
import json


class Bot:
    def __init__(self, number: str) -> None:
        self.requests = requests.session()
        self.number = number
        self.firstHeaders = {
            "authority": "api.divar.ir",
            "method": "POST",
            "path": "/v5/auth/verify",
            "scheme": "https",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
        }
        self.login()

    def req(self, url: str, data: dict) -> object:
        headers = {
            "authority": "api.divar.ir",
            "method": "POST",
            "scheme": "https",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "authorization": "Basic"+self.token,
        }

        return self.requests.post(url=url, headers=headers, json=data)

    def getCode(self) -> None:

        url = "https://api.divar.ir/v5/auth/authenticate"
        data = {"phone": self.number}
        
        return self.requests.post(url=url, headers=self.firstHeaders, json=data)

    def verfyCode(self) -> object:

        url = "https://api.divar.ir/v5/auth/confirm"
        data = {"phone": self.number, "code": input("Enter code: ")}

        return self.requests.post(url=url, headers=self.firstHeaders, json=data)

    def login(self) -> None:
        try:
            with open(f"{self.number}.json", 'r') as f:
                file = json.load(f)
                self.token = file["token"]
                self.access_token = file["access_token"]
                self.refresh_token = file["refresh_token"]
        except:
            self.getCode()
            with open(f"{self.number}.json", 'w') as f:
                dic = self.verfyCode().json()
                json.dump(dic, f)
                self.token = dic["token"]
                self.access_token = dic["access_token"]
                self.refresh_token = dic["refresh_token"]

    def getCategory(self, name: str) -> None:
        url = "https://api.divar.ir/v8/fields-search"
        data = {
            "q": name,
            "field": "category",
            "source": "submit"
        }
        return self.req(url, data)

    def setCategory(self, name: str) -> None:
        url = "https://api.divar.ir/v8/submit-v2/web-submit"

        data = {
            "default_values": {
                "data": {
                    "Category": {
                        "str": {
                            "value": self.getCategory(name).json()['results'][0]['enum']
                        }
                    },
                    "Location_CityId": {
                        "integer": {
                            "value": 1
                        }
                    }
                }
            },
            "page": 0,
            "widget_data_checksums": []
        }
        return self.req(url, data)
