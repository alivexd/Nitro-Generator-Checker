import aiohttp
import asyncio
import random
import string
import time
import multiprocessing

async def check_code(session, code):
    url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    async with session.get(url) as response:
        if response.status == 200:
            return f"https://discord.gift/{code} | Valid"
        else:
            return f"https://discord.gift/{code} | Invalid"

async def main(num_codes, valid_list, invalid_list, progress_queue):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_codes):
            code = "".join(random.choices(
                string.ascii_uppercase + string.digits + string.ascii_lowercase,
                k=16
            ))
            tasks.append(check_code(session, code))
            progress_queue.put(1)  # Increment the progress counter

        results = await asyncio.gather(*tasks)
        for result in results:
            if "Valid" in result:
                valid_list.append(result)
            else:
                invalid_list.append(result)

def run_main(num_codes, valid_list, invalid_list, progress_queue):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(num_codes, valid_list, invalid_list, progress_queue))

if __name__ == "__main__":
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
    print("Send Friend Request to Alive#1100 in case of bugs\n")
    time.sleep(0.2)

    num_total_codes = int(input("Input How Many Codes to Generate and Check: "))
    num_processes = multiprocessing.cpu_count()

    codes_per_process = num_total_codes // num_processes
    remaining_codes = num_total_codes % num_processes

    manager = multiprocessing.Manager()
    valid_list = manager.list()
    invalid_list = manager.list()
    progress_queue = manager.Queue()  # For progress tracking

    processes = []

    for process_id in range(num_processes):
        codes_to_generate = codes_per_process + (1 if process_id < remaining_codes else 0)
        process = multiprocessing.Process(target=run_main, args=(codes_to_generate, valid_list, invalid_list, progress_queue))
        processes.append(process)

    start = time.time()

    for process in processes:
        process.start()

    processed_codes = 0

    for process in processes:
        process.join()
        processed_codes += codes_per_process + (1 if process_id < remaining_codes else 0)
        print(f"Processed {processed_codes} codes out of {num_total_codes}")

    end = time.time()

    with open("Valid Codes.txt", "w", encoding='utf-8') as valid_file:
        for code_result in valid_list:
            valid_file.write(code_result + "\n")

    with open("Invalid Codes.txt", "w", encoding='utf-8') as invalid_file:
        for code_result in invalid_list:
            invalid_file.write(code_result + "\n")

    print(f"Generated and checked {num_total_codes} codes | Time taken: {end - start}\n")
    print(f"Valid codes saved to Valid Codes.txt")
    print(f"Invalid codes saved to Invalid Codes.txt")

    input("\nYou have generated. Now press enter to close this. You'll find valid and invalid codes with URLs in their respective files.")
