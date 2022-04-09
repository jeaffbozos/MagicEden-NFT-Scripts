import sys
import time
import requests
from tqdm import tqdm

delay = 0.51

def get_attr_floor(collection):
    price_map = {}
    attr_map = {}

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

    print(collection + ": Calculating attribute floors")
    for mint in tqdm(price_map.keys()):
        clock_since_call = time.time()
        try:
            url = "https://api-mainnet.magiceden.dev/v2/tokens/" + mint
            response = requests.request("GET", url)
            token = response.json()
            attrs = token['attributes']
        except:
            continue
        price = price_map[mint]

        for attr in attrs:
            attr = (str(attr['trait_type']), str(attr['value']))
            if attr not in attr_map:
                attr_map[attr] = price
            else:
                if price < attr_map[attr]:
                    attr_map[attr] = price

        #Delay minus time computing
        delay_since_call = time.time() - clock_since_call
        if delay_since_call < delay:
            time.sleep(delay - delay_since_call)

    return attr_map

def get_wallet_attrs(address, collections):
    nft_map = {}

    print("Fetching ME NFTs in wallet: " + address)
    i = 0
    while True:
        url = "https://api-mainnet.magiceden.dev/v2/wallets/" + address + "/tokens?offset=" + str(i*500) + "&limit=500"
        response = requests.request("GET", url)
        nfts = response.json()

        time.sleep(delay);
        if response.json() == []:
            break;

        for nft in nfts:
            try:
                if nft['collection'] in collections:
                    nft_map[nft['mintAddress']] = (nft['name'], nft['attributes'])
            except:
                print(nft['name'] + " not listed on ME (ignoring)")
                continue

        i+=1

    return nft_map

def get_price(attrs, attr_floor_map):

    max_value = 0
    #Getting highest value attribute
    for attr in attrs:
        attr = (str(attr['trait_type']), str(attr['value']))

        if attr in attr_floor_map:
            if attr_floor_map[attr] > max_value:
                max_value = attr_floor_map[attr]
        else:
            print("Attribute with no listings")

    return max_value

wallet_addr = sys.argv[1]

collections = sys.argv[2:]

attr_floor_map = get_attr_floor(collections[0])
wallet_map = get_wallet_attrs(wallet_addr, collections)

print("\n==========================Wallet Summary==========================")
print(collections[0])
sum = 0
for mint in wallet_map.keys():
    price = get_price(wallet_map[mint][1], attr_floor_map)
    print("\t" + wallet_map[mint][0] + ": " + str(price) + " SOL")
    sum += price

print("Total Attribute Floor Value: " + str(sum) + " SOL")
