import requests
import json
import time
import notify2

conf = open("./config/config.json")
config = json.load(conf)

#This value is added to the delay in case MagicEden thinks we are cutting too close into their TPS
#If you feel risky lower this value or make it 0
safety_delay = 0.05
delay = (1/config['TPS']) + safety_delay

#Returns a hasmap of the last list activites from the last config['activities_per_call'] activites
def init_collections():
    #Hasmap: Activity Signature => Activity
    ret = {}
    limit = config['activities_per_call']
    url = "http://api-mainnet.magiceden.dev/v2/collections/" + config['ME_symbol'] + "/activities?offset=0&limit=" + str(limit)
    response = requests.request("GET", url, headers={}, data={}).json()
    for x in response:
        if x['type'] == 'list':
            ret[x['signature']] = x
    return ret

#10**9
def get_price_floor():
    url = "https://api-mainnet.magiceden.dev/v2/collections/" + config['ME_symbol'] + "/stats"
    response = requests.request("GET", url, headers={}, data={}).json()
    return response['floorPrice']


#Send notification
def send_message(title, message):
    notify2.init("init")
    notif = notify2.Notification(title, message)
    notif.show()
    return

#===================================================================================================

#Getting initial state of sales
activities = init_collections()

#Add delay
time.sleep(delay)
#Get the current floor get_current_price
cur_floor = get_price_floor()

print(cur_floor)

#Getting the last blocktime to ensure no repeat NFTs are tweeted
last_blockTime =  list(activities.values())[0]['blockTime'] if len(activities) > 0 else 0
last_activities = activities

print(f"LISTENING FOR {config['ME_symbol'].upper()} LISTINGS")

#Bot loop
while True:
    #Getting hashmap
    try:
        activities = init_collections()
        time.sleep(delay)
    except:
        continue

    #Checking all activities (by signature, key values)
    for activity in activities.keys():
        #Checking if there is a new activity with a larger blockTime
        if activity not in last_activities.keys() and activities[activity]['blockTime'] >= last_blockTime:
            print(activities[activity]['price'] * 10**9)
            if activities[activity]['price'] * 10**9 < cur_floor:
                send_message("New listing under floor", "https://magiceden.io/item-details/" + activities[activity]['tokenMint'])
                print("New listing under floor: https://magiceden.io/item-details/" + activities[activity]['tokenMint'] + " for " + str(activities[activity]['price']))
                #Add delay
                time.sleep(delay)
                #Get the current floor get_current_price
                cur_floor = get_price_floor()

    last_blockTime =  list(activities.values())[0]['blockTime'] if len(activities) > 0 else 0
    last_activities = dict(activities)
