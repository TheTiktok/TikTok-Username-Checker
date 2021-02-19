import asyncio
import aiohttp
from typing import List
from os import system

def open_file() -> List[str]:
    with open('usernames.txt', 'r', encoding='UTF-8') as f:
        file_contents = [line.strip('\n') for line in f]

    return file_contents

def write_file(arg: str) -> None:
    with open('hits.txt', 'a', encoding='UTF-8') as f:
        f.write(f'{arg}\n')

class Checker:
    def __init__(self, usernames: List[str]):
        self.to_check = usernames

    async def _check(self, session: aiohttp.ClientSession, username: str) -> None:
        if len(username) > 2:        
            async with session.get('https://www.tiktok.com/@%s' % username) as response:
                try:
                    r = await response.text()
                    if response.status != 200 and 'trending' in r:
                        print('%s[AVAILABLE] https://www.tiktok.com/@%s%s' % ('\u001b[32;1m', username, '\u001b[0m'))
                        write_file(username)

                    elif response.status == 200 and 'trending' in r:
                        print('%s[UNAVAILABLE] https://www.tiktok.com/@%s%s' % ('\u001b[31;1m', username, '\u001b[0m'))

                    else:
                        if 'verify-ele' in r:
                            print('[!] Page needs to verify. Failed', username)
                            
                        else:
                            print('[!] No response. Most likely too many requests. Try again later', username)

                except Exception as e:
                    print('[ERROR] ' + e)
                    
    async def start(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for i in self.to_check:
                print('[*] Appending.. :', i)
                tasks.append(asyncio.create_task(self._check(session, i)))
            system('cls')
            print('Loading.. This may take awhile.')
            task = await asyncio.gather(*tasks)
            return task

if __name__ == '__main__':
    system('title TikTok Username Checker by Nightfall#2512')
    system('cls')
    username_list = open_file() 
    checker = Checker(username_list)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(checker.start())
