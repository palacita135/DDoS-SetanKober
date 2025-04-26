import requests

def fetch_proxies():
    """Fetch fresh proxies from ProxyScrape API and save to proxies.txt"""
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            proxies = response.text.strip().split("\n")
            
            if proxies:
                with open("proxies.txt", "w") as f:
                    f.write("\n".join(proxies))
                print(f"✅ Fetched {len(proxies)} fresh proxies and saved to proxies.txt")
            else:
                print("⚠ No proxies found!")
        else:
            print(f"❌ Failed to fetch proxies. Status code: {response.status_code}")

    except Exception as e:
        print(f"❌ Error fetching proxies: {e}")

# Run the proxy scraper
fetch_proxies()

