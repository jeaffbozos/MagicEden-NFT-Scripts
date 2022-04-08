import sys
import time
import requests

delay = 0.51

#Returns hasmap
def get_attr_floor(collection):
    #Hashmap storing mint and price
    price_map = {}
    #Hashmap storing attrs
    attr_map = {}

    i = 0
    while True:
        url = "https://api-mainnet.magiceden.dev/v2/collections/" + collection + "/listings?offset=" + str(i*20) + "&limit=20"
        response = requests.request("GET", url)
        listings = response.json()

        time.sleep(0.5);
        if response.json() == []:
            break;

        for listing in listings:
            price_map[listing['tokenMint']] = listing['price']

        i+=1


    print("MAPPING")
    for mint in price_map.keys():
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
            attr = str(attr['trait_type']) + "-" + str(attr['value'])
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



#Check valid
wallet_addr = sys.argv[2]

collections = sys.argv[2:]

print(collections)


get_attr_floor(collections[0])
