import sys
import time
import requests
from tqdm import tqdm

delay = 0.5

def delay_call(clock_since_call):
    delay_since_call = time.time() - clock_since_call
    if delay_since_call < delay:
        time.sleep(delay - delay_since_call)

def get_price_map(collection):
    price_map = {}
    print(f"{collection}: Fetching current listings (this will take a minute)")
    i = 0
    while True:
        clock_since_call = time.time()
        url = "https://api-mainnet.magiceden.dev/v2/collections/" + collection + "/listings?offset=" + str(i*20) + "&limit=20"
        response = requests.request("GET", url)
        listings = response.json()

        if response.json() == []:
            break;

        for listing in listings:
            price_map[listing['tokenMint']] = listing['price']

        delay_call(clock_since_call)

        i+=1

    return price_map

def get_hr_map(HR_symbol):
    attr_map = {}

    url = "https://api.howrare.is/v0.1/collections/" + HR_symbol
    try:
        response = requests.request("GET", url)
        response = response.json()
        items = response['result']['data']['items']

        for nft in items:
            try:
                attr_map[nft['mint']] = int(nft['attributes'][0]['value'])
            except:
                continue
    except:
        return None

    return attr_map

def get_floor_hr(price_map, HR_symbol):
    hr_map = get_hr_map(HR_symbol)
    attr_map = {}
    errors = []
    print("Fetching token attributes")

    for mint in tqdm(price_map.keys()):

        if hr_map[mint] not in attr_map:
            attr_map[hr_map[mint]] = (price_map[mint], mint)
        else:
            if attr_map[hr_map[mint]][0] > price_map[mint]:
                attr_map[hr_map[mint]] = (price_map[mint], mint)

    return attr_map


def get_floor(price_map):
    attr_map = {}
    errors = []
    print("Fetching token attributes")

    for mint in tqdm(price_map.keys()):
        try:
            clock_since_call = time.time()
            url = "https://api-mainnet.magiceden.dev/v2/tokens/" + mint
            response = requests.request("GET", url)
            metadata = response.json()

            attr_count = 0
            for attr in metadata['attributes']:
                if attr['value'] != "None":
                    attr_count += 1

            if attr_count not in attr_map:
                attr_map[attr_count] = (price_map[mint], mint)
            else:
                if attr_map[attr_count][0] > price_map[mint]:
                    attr_map[attr_count] = (price_map[mint], mint)
        except:
            errors.append(mint)

        delay_call(clock_since_call)

    return (attr_map, errors)


price_map = get_price_map(sys.argv[1])

if len(sys.argv) > 2:
    floor = get_floor_hr(price_map, sys.argv[2])
    errors = []
else:
    (floor, errors) = get_floor(price_map)


print("=================================================================")
print(f"{sys.argv[1]} attribute count floors on MagicEden")

for k, v in sorted(floor.items()):
    print(f"Attribute count: {k}, floor price: {v[0]} SOL")
    print(f"    -https://magiceden.io/item-details/{v[1]}")

print("=================================================================")

if len(errors):
    print(f"Error with mint addresses: " + errors)
