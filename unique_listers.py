import sys
import time
import requests

delay = 0.5

def unique_sellers(collection):
    holders = {}
    price_map = {}
    print(f"{collection}: Fetching current listings (this will take a minute)")
    i = 0
    while True:
        url = "https://api-mainnet.magiceden.dev/v2/collections/" + collection + "/listings?offset=" + str(i*20) + "&limit=20"
        response = requests.request("GET", url)
        listings = response.json()

        time.sleep(delay);
        if response.json() == []:
            break;

        for listing in listings:
            if listing['seller'] not in holders.keys():
                holders[listing['seller']] = [listing['tokenMint']]
            else:
                holders[listing['seller']].append(listing['tokenMint'])
            price_map[listing['tokenMint']] = listing['price']


        i+=1

    return (holders, price_map)


(un_sellers, price_map) = unique_sellers(sys.argv[1])

print("=================================================================")

print(f"Largest {sys.argv[1]} sellers on MagicEden")


for k in sorted(un_sellers, key=lambda k: len(un_sellers[k]), reverse=True):
    print("(" + str(len(un_sellers[k])) + ") https://solscan.io/account/" + k)
    for mint in un_sellers[k]:
        print(f"    - ({str(price_map[mint])} SOL) https://magiceden.io/item-details/{mint}")


print("=================================================================")
