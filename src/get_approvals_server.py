import asyncio
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from utils import Utils

COIN_API_KEY = 'CG-HsbhtP7VhoXbN5Dyszu9FR4q'
COIN_API_URL = 'https://api.coingecko.com/api/v3/simple/price?ids={name}&vs_currencies=usd'
INFURA_KEY = 'f7db56ffa69c44acab30f3bd83252d8e'
DECIMALS = 18

app = FastAPI()


async def async_task(address: str, utils: Utils, start_block: Optional[int] = None, end_block: Optional[int] = None):
    approval_logs = []
    if start_block or end_block:
        if not start_block:
            raise HTTPException(status_code=500,
                                detail='end block was not given,  you must enter a start block and an end block')
        elif not end_block:
            raise HTTPException(status_code=500,
                                detail='end block was not given,  you must enter a start block and an end block')
    logs = utils.get_approval_logs(address, start_block, end_block)
    for log in logs:
        owner = utils.web3.to_checksum_address(log['topics'][1].hex()[-40:])
        spender = utils.web3.to_checksum_address(log['topics'][2].hex()[-40:])
        block_number = log['blockNumber']
        value_hex = log["data"].hex()
        value_decimal = str(int(value_hex, 16)).zfill(2 * DECIMALS)
        value_decimal = value_decimal[:-DECIMALS] + '.' + value_decimal[-DECIMALS:]
        approval_logs.append(
            {'owner': owner, 'spender': spender, 'blockNumber': block_number, 'value': value_decimal})
    return {"address": address, "startBlock": start_block, "endBlock": end_block, 'logs': approval_logs}


@app.get("/get_approvals")
async def get_approvals(address: str, start_block: Optional[int] = None, end_block: Optional[int] = None):
    try:
        utils = Utils(INFURA_KEY)
        tasks = []
        for add in address.split('^'):
            tasks.append(async_task(add, utils, start_block, end_block))
        results = await asyncio.gather(*tasks)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_coin")
async def get_coin(name: str):
    try:
        response = requests.get(COIN_API_URL.format(name=name.lower()))

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch data from the coin API")

        coin_data = response.json()

        if not coin_data:
            raise HTTPException(status_code=404, detail="Coin not found in the API")

        coin_info = coin_data.get(name.lower())
        if not coin_info:
            raise HTTPException(status_code=404, detail="Coin not found in the API response")

        return {"name": name, "price": coin_info.get('usd')}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from the API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the FastAPI app, use `uvicorn` command:
# uvicorn your_script_name:app --reload


# {
#     "bitcoin": {
#         "usd": 60620
#     }
# }
