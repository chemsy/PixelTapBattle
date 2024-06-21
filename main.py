import asyncio
import os
import json
import sys
from Battle import Battle
from Pixelverse import UserPixel
from random import randint
from colorama import Fore, Style, init 
from time import sleep

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
clear()

def split_chunk(var):
    if isinstance(var, int):
        var = str(var)
    n = 3
    var = var[::-1]
    return ' '.join([var[i:i + n] for i in range(0, len(var), n)])[::-1]

async def main():
    try:
        init()
        user = UserPixel()
        users = user.getUsers()
        stats = user.getStats()
        winRate = (stats['wins'] / stats['battlesCount']) * 100
        dailyRewards = user.getDailyRewards()
        claimDailyRewards = user.claimDailyRewards()
        claim = user.claim()
        # pets = user.getPets()
        
        print(f"👻 {Fore.MAGENTA+Style.BRIGHT}[ User ]\t\t: {Fore.RED+Style.BRIGHT}[ Username ] {users['username']}")
        user.claim()
        print(f"👻 {Fore.MAGENTA+Style.BRIGHT}[ User ]\t\t: {Fore.RED+Style.BRIGHT}[ Balance ] {split_chunk(str(int(users['clicksCount'])))}")
        print(f"👻 {Fore.MAGENTA+Style.BRIGHT}[ User Stats ]\t: {Fore.GREEN+Style.BRIGHT}[ Wins ] {split_chunk(str(stats['wins']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.RED+Style.BRIGHT}[ Loses ] {split_chunk(str(stats['loses']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Battles Count ] {split_chunk(str(stats['battlesCount']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.WHITE+Style.BRIGHT}[ Winrate ] {winRate:.2f}%")
        print(f"👻 {Fore.MAGENTA+Style.BRIGHT}[ User Stats ]\t: {Fore.GREEN+Style.BRIGHT}[ Wins Reward ] {split_chunk(str(stats['winsReward']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.RED+Style.BRIGHT}[ Loses Reward ] {split_chunk(str(stats['losesReward']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Total Earned ] {split_chunk(str(stats['winsReward'] + stats['losesReward']))}")
        print(f"💰 {Fore.CYAN+Style.BRIGHT}[ Daily Reward ]\t: {Fore.GREEN+Style.BRIGHT}[ Total Claimed ] {split_chunk(str(dailyRewards['totalClaimed']))} Coins")
        print(f"💰 {Fore.CYAN+Style.BRIGHT}[ Daily Reward ]\t: {Fore.GREEN+Style.BRIGHT}[ Day ] {split_chunk(str(dailyRewards['day']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Reward Amount ] {split_chunk(str(dailyRewards['rewardAmount']))} Coins")
        print(f"💰 {Fore.CYAN+Style.BRIGHT}[ Daily Reward ]\t: {Fore.GREEN+Style.BRIGHT}[ Next Day ] {split_chunk(str(dailyRewards['nextDay']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Next Day Reward Amount ] {split_chunk(str(dailyRewards['nextDayRewardAmount']))} Coins")
        if dailyRewards['todaysRewardAvailable'] == True:
            print(f"💰 {Fore.CYAN+Style.BRIGHT}[ Daily Reward ]\t: {Fore.GREEN+Style.BRIGHT}[ Todays Reward Available ] Available")
            print(f"💰 {Fore.CYAN+Style.BRIGHT}[ Daily Reward ]\t: {Fore.GREEN+Style.BRIGHT}[ Claiming ] | [ Day ] {claimDailyRewards['day']} | [ Amount ] {claimDailyRewards['amount']}\n")
            user.claimDailyRewards()
        else:
            print(f"💰 {Fore.CYAN+Style.BRIGHT}[ Daily Reward ]\t: {Fore.RED+Style.BRIGHT}[ Todays Reward Available ] Not Available\n")
        # for pet in pets:
        #     print(f"🐈 {Fore.GREEN+Style.BRIGHT}[ Pets ]\t\t: [ Name ] {pet['name']} | [ Level ] {pet['userPet']['level']} | [ Level Up Price ] {pet['userPet']['levelUpPrice']} | [ Energy ] {pet['userPet']['energy']} | [ Max Energy ] {pet['userPet']['maxEnergy']}")

        with open('./config.json', 'r') as config_file:
            config = json.load(config_file)
        
        battle = Battle()
        await battle.connect()
        del battle

        user.upgradePets(auto_upgrade=config['auto_upgrade'])
        
        clear()
    except Exception as e:
        print(e)
        clear()

if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print(f"👋🏻 [ Dadah ]")
            sys.exit(0)
        except Exception as e:
            if UserPixel().isBroken():
                print(f"🤖 {Fore.RED+Style.BRIGHT}[ Bot ]\t\t: The server seems down, restarting")
                sleep(randint(5, 10)*5)
            else:
                print(f"🤖 {Fore.RED+Style.BRIGHT}[ Bot ]\t\t: {type(e).__name__} - {e}")
                sleep(randint(5, 10))
            clear()