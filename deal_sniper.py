import sys
import time
import requests

delay = 0.51

def get_attr_floor(collection):
    price_map = {}
    print(collection + ": Fetching current listings (this will take a minute)")
    i = 0
    while True:
        url = "https://api-mainnet.magiceden.dev/v2/collections/" + collection + "/listings?offset=" + str(i*20) + "&limit=20"
        response = requests.request("GET", url)
        listings = response.json()

        time.sleep(delay);
        if response.json() == []:
            break;

        for listing in listings:
            price_map[listing['tokenMint']] = listing['price']

        i+=1

    return price_map

def get_rarity(collection):
    url = "https://api.howrare.is/v0.1/collections/" + collection
    try:
        response = requests.request("GET", url)
        response = response.json()
        data = response['result']['data']['items']
    except:
        return None

    size = len(data)

    rarity = {}

    for nft in data:
        rarity[nft['mint']] = nft['rank']

    return rarity

def get_rarity_price(rarity_map, price_map):
    rarity_price_map = {}

    size = len(rarity_map.keys())

    for mint in price_map.keys():
        rarity_price_map[mint] = (float(rarity_map[mint]) / size) * price_map[mint]

    return rarity_price_map


ME_name = sys.argv[1]

HR_name = sys.argv[2]

top_n = 10 if len(sys.argv) <= 3 else int(sys.argv[3])

price_map = get_attr_floor(ME_name)
rarity_map = get_rarity(HR_name)
rarity_price_map = get_rarity_price(rarity_map, price_map)

deals = dict(sorted(rarity_price_map.items(), key=lambda item: item[1]))

print("=================================================================")

print("Top " + str(top_n) + " " + ME_name + " deals on MagicEden")

top_deals = list(deals.keys())[:top_n]
for i in range(0, len(top_deals)):
    print("\t- Rank " + str(rarity_map[top_deals[i]]) + ", " + str(price_map[top_deals[i]]) + " SOL: https://magiceden.io/item-details/" + top_deals[i])

print("=================================================================")
