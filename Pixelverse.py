import json
import requests
from colorama import Fore, Style
from time import sleep

def split_chunk(var):
    if isinstance(var, int):
        var = str(var)
    n = 3
    var = var[::-1]
    return ' '.join([var[i:i + n] for i in range(0, len(var), n)])[::-1]

class UserPixel:
    def __init__(self):
        with open('./config.json', 'r') as file:
            self.config = json.load(file)
        
        self.headers = {
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "api-clicker.pixelverse.xyz",
            "If-None-Match": 'W/"29b-JPcgLG/Nvfd8KEVQN/lMKfPaHpQ"',
            "initData": self.config['initData'],
            "Origin": "https://sexyzbot.pxlvrs.io",
            "Priority": "u=3, i",
            "Referer": "https://sexyzbot.pxlvrs.io/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "secret": self.config['secret'],
            "tg-id": self.config['tgId'],
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)"
        }

    def getUsers(self):
        url = "https://api-clicker.pixelverse.xyz/api/users"
        req = requests.get(url, headers=self.headers)
        return req.json()

    def getStats(self):
        url = "https://api-clicker.pixelverse.xyz/api/battles/my/stats"
        req = requests.get(url, headers=self.headers)
        return req.json()
    
    def getPets(self):
        data = self.getUsers()
        url = "https://api-clicker.pixelverse.xyz/api/pets"
        req = requests.get(url, headers=self.headers)
        data = req.json()
        return data['data']

    def upgrade(self, petId: str):
        url = f"https://api-clicker.pixelverse.xyz/api/pets/user-pets/{petId}/level-up"
        req = requests.post(url, headers=self.headers)
        return req.json()

    def upgradePets(self, auto_upgrade: bool):
        data = self.getUsers()
        currBalance = data['clicksCount']
        url = "https://api-clicker.pixelverse.xyz/api/pets"
        req = requests.get(url, headers=self.headers)
        pets = req.json()['data']
        for pet in pets:
            if auto_upgrade:
                if pet['userPet']['isMaxLevel'] == True:
                    print(f"🐈 {Fore.GREEN+Style.BRIGHT}[ Pets ]\t\t: [ {pet['name']} ] Is Max Level")
                else:
                    if currBalance >= pet['userPet']['levelUpPrice']:
                        self.upgrade(pet['userPet']['id'])
                        print(f"🐈 {Fore.GREEN+Style.BRIGHT}[ Pets ]\t\t: [ {pet['name']} ] Success Level Up")
                        sleep(0.5)
                    else:
                        print(f"🐈 {Fore.YELLOW+Style.BRIGHT}[ Pets ]\t\t: Not Enough Coins To Upgrade [ {pet['name']} ] {(split_chunk(str(int(pet['userPet']['levelUpPrice'] - data['clicksCount']))))} Coins Remaining")
            else:
                print(f"🐈 {Fore.GREEN+Style.BRIGHT}[ Pets ]\t\t: [ {pet['name']} ] Can Upgrade")

    def claim(self):
        url = "https://api-clicker.pixelverse.xyz/api/mining/claim"
        req = requests.post(url, headers=self.headers)
        return req.json()
    
    def getDailyRewards(self):
        url = "https://api-clicker.pixelverse.xyz/api/daily-rewards"
        req = requests.get(url, headers=self.headers)
        return req.json()

    def claimDailyRewards(self):
        url = "https://api-clicker.pixelverse.xyz/api/daily-rewards/claim"
        req = requests.post(url, headers=self.headers)
        return req.json()

    def isBroken(self):
        url = "https://api-clicker.pixelverse.xyz/api/tasks/my"
        req = requests.get(url, headers=self.headers)
        return req.status_code == 500