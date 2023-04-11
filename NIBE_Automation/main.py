import pandas as pd
from datetime import datetime
from time import sleep
from json import dump, load
from requests_oauthlib import OAuth2Session
from energy_price import ElectricityPricing

price_collector = ElectricityPricing() 

HTTP_STATUS_OK = 200 #En statuskode returneret af API
client_id = '59682261e9f04ab9a867eb7cfa93e840' # (32 hex digits)
client_secret = '/xADpEzVVYraWKnP6lZvcbT2RX51N4TDSM34Lry+w7w=' # (44 characters)
token_filename= '.NIBE_Uplink_API_Token_PUT.json'
token_url = 'https://api.nibeuplink.com/oauth/token'
extra_args = {'client_id': client_id, 'client_secret': client_secret}


def token_saver(token):
    '''Token stuff, bruges til at opdatere token efter en request på api'''
    with open(token_filename, 'w') as token_file:
        dump(token, token_file)

with open(token_filename, 'r') as token_file:
    token = load(token_file)


nibeuplink = OAuth2Session(client_id=client_id, token=token, auto_refresh_url=token_url, auto_refresh_kwargs=extra_args, token_updater=token_saver)


def gettime():
    now = datetime.now()

    current_time = now.strftime("%H")
    return(current_time)

def getstatus(index):
    df = pd.read_csv('combineddata.csv')
    try:
        value = df['TurnOn'].iloc[index]
        return(value)
    except Exception as e:
        return(e)


url = 'https://api.nibeuplink.com/api/v1/systems/138372/parameters/'

time = int(gettime())
status = getstatus(time)
print(status)
print("Current time is ", time)
if status == "True":
    query = {
        'settings':{
        '47011':'10'
        }
    }
    print("Heat pump set to: 10")
elif status == "False":
    query = {
        'settings':{
        '47011':'-10'
        }
    }
    print("Heat pump set to: -10")
elif status == "Normal":
    query = {
        'settings':{
        '47011':'0'
        }
    }
    print("Heat pump set to: 0")
response = nibeuplink.put(url, json=query)
if response.status_code == HTTP_STATUS_OK:
    print("HTTP Status: OK", "\n200")
else:
    print('HTTP Status: ' + str(response.status_code))
    print(response.text)
sleep(5*60)

