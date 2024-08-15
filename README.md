## Prerequisites:
`pip install -r requirements.txt`


## Running the script:
`cd src`  
`python get_approvals_script.py`  

#### Notes:
* the delimiter for addresses is `^` use it in the param query for multiple addresses  
* params for the script are:
  * address - the address to query for - mandatory
  * start-block - the block to query from - optional(will take latest if not given)
  * end-block - the blok to query to - optional(will take latest if not given)
### example: 
`python get_approvals_script.py --address=0xcd90574bc2ef39bcebbc5561c1c9d8e42110c239 --start-block=20505574 --end-block=20509574`


## Running the web server:
`cd src`  
`uvicorn get_approvals_server:app`  
### get_approvals endpoint:  
#### Notes:  
* the delimiter for addresses is `^` use it in the param query for multiple addresses  
* query params are:
  * addresses - the addresses to query for - mandatory
  * start_block - the block to query from - optional(will take latest if not given)
  * end_block - the blok to query to - optional(will take latest if not given)
#### example:
`curl --location 'http://127.0.0.1:8000/get_approvals?address=0xcd90574bc2ef39bcebbc5561c1c9d8e42110c239%5E0x6C395f5c062Ed0297DC57A7A270B1a950C4DcE46&start_block=20505574&end_block=20509874'`
### get_coin endpoint:
#### Notes:  
* Query params are:
  * name - the name of the coin  
#### example: 
`curl --location 'http://127.0.0.1:8000/get_coin?name=bitcoine'`
