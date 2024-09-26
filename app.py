from colorama import *
from datetime import datetime, timedelta
from requests import (
    JSONDecodeError,
    RequestException,
    Session
)
import asyncio
import json
import os
import sys

class Seed:
    def __init__(self) -> None:
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'elb.seeddao.org',
            'Origin': 'https://cf.seeddao.org',
            'Pragma': 'no-cache',
            'Referer': 'https://cf.seeddao.org/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_timestamp(self, message):
        print(
            f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL} | {message}",
            flush=True
        )

    def load_queries(self):
        """
        Load queries from queries.txt file. Each line represents a different query.
        """
        if not os.path.exists('queries.txt'):
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ queries.txt file not found! Please create the file and add queries. ]{Style.RESET_ALL}")
            sys.exit(1)
        
        with open('queries.txt', 'r') as file:
            queries = [line.strip() for line in file.readlines() if line.strip()]
        return queries

    def print_custom_banner(self):
        print(Fore.YELLOW + "===================================" + Style.RESET_ALL)
        print(Fore.YELLOW + "  Trick Alert 🔥  Auto Claimer" + Style.RESET_ALL)
        print(Fore.YELLOW + "  Join our Telegram Channel: " + Style.RESET_ALL + Fore.GREEN + "https://t.me/Trickalert" + Style.RESET_ALL)
        print(Fore.YELLOW + "===================================" + Style.RESET_ALL)

        # زخرفة الدولار
        print(Fore.GREEN + """
             $$$$$$$$$$$$$$$$$$$$$$$$$$$$
             $$                       $$   
             $$     $$$$$$$$$$$$$      $$ 
             $$    $$$        $$$$     $$ 
             $$   $$$          $$$     $$ 
             $$   $$$          $$$     $$ 
             $$    $$$        $$$$     $$ 
             $$     $$$$$$$$$$$$$      $$ 
             $$                       $$   
             $$$$$$$$$$$$$$$$$$$$$$$$$$$$
        """ + Style.RESET_ALL)

    async def profile(self, query: str):
        url = 'https://elb.seeddao.org/api/v1/profile'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'telegram-data': query
        }
        try:
            with Session().post(url=url, headers=headers) as response:
                response.raise_for_status()
                return True
        except (Exception, JSONDecodeError, RequestException):
            return False

    async def profile2(self, query: str):
        url = 'https://elb.seeddao.org/api/v1/profile2'
        headers = {
            **self.headers,
            'telegram-data': query
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                profile2 = response.json()['data']
                if not profile2['give_first_egg']:
                    return await self.give_first_egg(query=query)
        except (JSONDecodeError, RequestException) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Profile: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Profile: {str(e)} ]{Style.RESET_ALL}")

    async def give_first_egg(self, query: str):
        url = 'https://elb.seeddao.org/api/v1/give-first-egg'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'telegram-data': query
        }
        try:
            with Session().post(url=url, headers=headers) as response:
                give_first_egg = response.json()['data']
                if give_first_egg['status'] == 'in-inventory':
                    self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {give_first_egg['type']} From Give First Egg ]{Style.RESET_ALL}")
                    return await self.complete_egg_hatch(query=query, egg_id=give_first_egg['id'])
        except (JSONDecodeError, RequestException) as e:
            if e.response.status_code == 400:
                return self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Already Received Give First Egg ]{Style.RESET_ALL}")
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Give First Egg: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Give First Egg: {str(e)} ]{Style.RESET_ALL}")

    async def balance_profile(self, query: str):
        url = 'https://elb.seeddao.org/api/v1/profile/balance'
        headers = {
            **self.headers,
            'telegram-data': query
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                return response.json()['data']
        except (JSONDecodeError, RequestException) as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Profile Balance: {str(e)} ]{Style.RESET_ALL}")
            return None
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Profile Balance: {str(e)} ]{Style.RESET_ALL}")
            return None

    async def claim_seed(self, query: str):
        url = 'https://elb.seeddao.org/api/v1/seed/claim'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'telegram-data': query
        }
        try:
            with Session().post(url=url, headers=headers) as response:
                response.raise_for_status()
                claim_seed = response.json()['data']
                return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {claim_seed['amount'] / 1000000000} From Seeding ]{Style.RESET_ALL}")
        except (JSONDecodeError, RequestException) as e:
            if e.response.status_code == 400:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Claim Seed Too Early ]{Style.RESET_ALL}")
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Seed: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Seed: {str(e)} ]{Style.RESET_ALL}")

    async def main(self):
        self.print_custom_banner()
        while True:
            try:
                # تحميل الاستعلامات من الملف
                queries = self.load_queries()
                if not queries:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ No queries found in queries.txt ]{Style.RESET_ALL}")
                    return

                total_balance = 0.0
                for query in queries:
                    self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ Processing query ]{Style.RESET_ALL}")
                    await self.profile(query=query)
                    await self.profile2(query=query)
                    await self.claim_seed(query=query)
                    balance = await self.balance_profile(query=query)
                    total_balance += float(balance / 1000000000) if balance else 0.0

                self.print_timestamp(
                    f"{Fore.CYAN + Style.BRIGHT}[ Total Queries {len(queries)} ]{Style.RESET_ALL} | "
                    f"{Fore.GREEN + Style.BRIGHT}[ Total Balance {total_balance} ]{Style.RESET_ALL}"
                )

                # الانتظار بين الدورات
                await asyncio.sleep(15 * 60)
                self.clear_terminal()

            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
                continue

if __name__ == '__main__':
    try:
        init(autoreset=True)
        seed = Seed()
        asyncio.run(seed.main())
    except (ValueError, IndexError, FileNotFoundError) as e:
        seed.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)
