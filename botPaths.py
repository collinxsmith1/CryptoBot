import os
import subprocess
import json
import ast

HERE = os.getcwd()
DATADIR = "data"
AUTHDIR = "auth"
TMP = "/tmp"

#%% DIRECTORY PATHS #######################################################################

dataPath = os.path.join(HERE, DATADIR) # directory to crypto data
if not os.path.exists(dataPath):
    os.makedirs(dataPath)

authPath = os.path.join(HERE, AUTHDIR)
if not os.path.exists(authPath):
    os.makedirs(authPath)

cryptoDataDir = os.path.join(dataPath, 'cryptoData')
if not os.path.exists(cryptoDataDir):
    os.makedirs(cryptoDataDir)

coinGeckoCoinJson = os.path.join(cryptoDataDir, 'coinGeckoCoinList.json')
coinGeckoCoinJson_Icons = os.path.join(cryptoDataDir, 'coinGeckoCoinList_Icons.json')

coinSubsListJson = os.path.join(cryptoDataDir, 'coinSubsList.json')
coinSubsListJsonNew = os.path.join(cryptoDataDir, 'coinSubsListNew.json')
coinSubsListJson2 = os.path.join(cryptoDataDir, 'coinSubsList2.json')
coinTrackListJson = os.path.join(cryptoDataDir, 'coinTrackList.json')
coinTrackListJsonNew = os.path.join(cryptoDataDir, 'coinTrackListNew.json')

cryptoDataCoins = os.path.join(cryptoDataDir, 'coins')
if not os.path.exists(cryptoDataCoins):
    os.makedirs(cryptoDataCoins)

if os.path.exists(coinGeckoCoinJson):
    with open(coinGeckoCoinJson, 'r') as rf:
        coinGeckoCoinList = json.loads(rf.read())

else:
    ### Init coingecko.com API list of coins to file. https://www.coingecko.com/en/api/pricing

    url = 'https://api.coingecko.com/api/v3/coins/list'
    # curl -X GET "https://api.coingecko.com/api/v3/coins/ethereum?localization=false" -H "accept: application/json"
    curlcommand = ["curl", "-X", "GET", "https://api.coingecko.com/api/v3/coins/list", "-sb", "-H", "accept: application/json"]

    result = subprocess.run(curlcommand,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    
    response = result.stdout.decode() # string
    coinGeckoCoinList = ast.literal_eval(response)

    with open(coinGeckoCoinJson, 'w') as wf:
        json.dump(coinGeckoCoinList, wf)

if os.path.exists(coinGeckoCoinJson_Icons):
    with open(coinGeckoCoinJson_Icons, 'r') as rf:
        coinGeckoCoinList_Icons = json.loads(rf.read())

