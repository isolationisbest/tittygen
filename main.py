import aiohttp
import asyncio
import random
import string
import colorama
import sys

valid_codes = []
codes_per_second = 25  # Generate 100 codes per second

async def check_code(session, code):
    async with session.get(f'https://discord.com/api/v10/entitlements/gift-codes/{code}') as response:
        if response.status == 200:
            valid_codes.append(code)
            with open('valid.txt', 'a') as valid_file:
                valid_file.write(f"https://discord.com/gifts/{code}\n")
            print(f"{colorama.Fore.LIGHTGREEN_EX}VALID{colorama.Fore.RESET} | https://discord.com/gifts/{code}")
            return True  # A valid code is found
        else:
            print(f"{colorama.Fore.LIGHTRED_EX}INVALID{colorama.Fore.RESET} | https://discord.com/gifts/{code}")

async def generate_and_check():
    async with aiohttp.ClientSession() as session:
        code_found = False
        while not code_found:
            tasks = []
            for _ in range(codes_per_second):
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
                task = check_code(session, code)
                tasks.append(task)

            results = await asyncio.gather(*tasks)
            code_found = any(results)

if __name__ == '__main__':
    colorama.init(autoreset=True)  # Initialize colorama for colored output
    asyncio.run(generate_and_check())