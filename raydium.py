import pandas as pd
import numpy as np
import solana
import plotly as plt
from dotenv import load_dotenv, find_dotenv
import os

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
    print(f'endPoint: {endPoint}')
else:
    print("endPoint variable not found")
