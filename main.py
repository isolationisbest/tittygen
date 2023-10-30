import aiohttp
import asyncio
import random
import string
from termcolor import colored

# Number of codes to generate and check.
num_codes = int(input("Enter the number of codes to generate and check: "))

valid_codes = []
invalid_codes = []

async def check_code(session, code):
    async with session.get(f'https://discord.com/api/v10/entitlements/gift-codes/{code}') as response:
        if response.status == 200:
            valid_codes.append(code)
        elif response.status == 404:
            invalid_codes.append(code)

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [check_code(session, ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)) ) for _ in range(num_codes)]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())

print("\n\033[1m\033[4mtitty gen\033[0m | Invalid: \033[91m{}\033[0m codes generated | Found: \033[92m{}\033[0m codes generated".format(len(invalid_codes), len(valid_codes)))

print("\nValid Nitro Codes:")
for code in valid_codes:
    code_url = f"https://discord.com/gifts/{code}"
    colored_code_url = colored(code_url, 'green')
    print(colored("VALID |", 'green'), colored_code_url)

print("\nInvalid Nitro Codes:")
for code in invalid_codes:
    code_url = f"https://discord.com/gifts/{code}"
    colored_code_url = colored(code_url, 'red')
    print(colored("INVALID |", 'red'), colored_code_url)