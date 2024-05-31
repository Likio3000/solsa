import pandas as pd
import numpy as np
import solana
import plotly as plt
from dotenv import load_dotenv, find_dotenv
import os
import json
import time
import logging
import threading
import urllib.request
import json
from urllib.request import Request, urlopen
from solana.rpc.api import Client


# PARTE 1: IMPORTAR EL ENDPOINT/NODO DEL .ENV

# Find and load the .env file
dotenv_path = find_dotenv("settings.env")
if dotenv_path:
    load_dotenv(dotenv_path)
    print("Loaded .env file from:", dotenv_path)
else:
    print("Could not find .env file")

# Access the .env variables
endPoint = os.getenv("endPoint")

if endPoint:
    print("I've got an endPoint to work with")
else:
    print("endPoint variable not found")



# PARTE 2:  HACER LA INICIALIZACION PARA ESCUCHAR


explorerULRAdd = "https://explorer.solana.com/address/"
explorerULRTx = "https://explorer.solana.com/tx/"

Address_RaydiumAMM = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
Address_liquidityPool = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
Address_solscan = "https://api.solscan.io/account?address="

#HTTP CLIENT
http_client = Client(endPoint)



# PARTE 3: ESCUCHAR LA DATA, Y "RETENERLA":


lastSignature = None
resultArr = []
rounds = 0
txCount = 0
maxTxCount = 1000 #about 1 min
Address_RaydiumAMM = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"

def getTxDetail(txSignature):
    txSignature2 = solana.transaction.Signature.from_string(txSignature)
    tx = http_client.get_transaction(txSignature2,max_supported_transaction_version=0)
    tx = json.loads(tx.to_json())
    postTokenBalances = tx["result"]["meta"]["postTokenBalances"]
    preTokenBalances = tx["result"]["meta"]["preTokenBalances"]
    if (postTokenBalances != preTokenBalances):
        print(explorerULRTx+txSignature)
        resultArr.append(tx)


# Getting all transactions
if __name__ == "__main__":
    RaydiumPubKey = solana.rpc.types.Pubkey.from_string(Address_RaydiumAMM)
    while(True):
        print("round-"+str(rounds+1))
        print("getting transactions")
        RaydiumPubKey = solana.rpc.types.Pubkey.from_string(Address_RaydiumAMM)
        txs = http_client.get_signatures_for_address(RaydiumPubKey,limit=200,before=lastSignature).to_json()
        txs = json.loads(txs) ["result"]
        print("processing signatures")
        signatures = np.array([o["signature"] for o in txs])

        threads = list()
        for signature in signatures:
            txCount += 1
            x = threading.Thread(target=getTxDetail, args=(signature,))
            threads.append(x)
            x.start()
        for index, thread in enumerate(threads):
            thread.join()
        if(txCount >= maxTxCount):
            break
        else:
            rounds += 1
            lastSignature = solana.transaction.Signature.from_string(txs[-1]["signature"])
        time.sleep(3)