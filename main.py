
import requests
import random
import string
import time

print("""
░█████╗░██╗░░░░░██╗██╗░░░██╗███████╗
██╔══██╗██║░░░░░██║██║░░░██║██╔════╝
███████║██║░░░░░██║╚██╗░██╔╝█████╗░░
██╔══██║██║░░░░░██║░╚████╔╝░██╔══╝░░
██║░░██║███████╗██║░░╚██╔╝░░███████╗
╚═╝░░╚═╝╚══════╝╚═╝░░░╚═╝░░░╚══════╝""")
time.sleep(2)
print("Generating Nitro Links")
time.sleep(0.3)
print("Join discord.gg/dignity For More\n")
time.sleep(0.2)

num = int(input('Input How Many Codes to Generate and Check: '))

with open("Nitro Codes.txt", "w", encoding='utf-8') as file:
    print("Your nitro codes are being generated, be patient if you entered the high number!")

    start = time.time()

    for i in range(num):
        code = "".join(random.choices(
            string.ascii_uppercase + string.digits + string.ascii_lowercase,
            k = 16
        ))

        file.write(f"https://discord.gift/{code}\n")

    print(f"Generated {num} codes | Time taken: {time.time() - start}\n")

with open("Nitro Codes.txt") as file:
    for line in file.readlines():
        nitro = line.strip("\n")

        url = "https://discordapp.com/api/v6/entitlements/gift-codes/" + nitro + "?with_application=false&with_subscription_plan=true"

        r = requests.get(url)

        if r.status_code == 200:
            print(f" Valid | {nitro} ")
            break
        else:
            print(f" Invalid | {nitro} ")

input("\nYou have generated, Now press enter to close this, you'll get valid codes in Valid Codes.txt if you see its empty then you got no luck, generate 20 million codes for luck or else.")
