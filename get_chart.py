import cufflinks as cf
from binance.client import Client
import pandas as pd
from datetime import datetime
import json 
import telegram_send

## Configuration variables
api_key, api_secret = "",""

pairs = ["GMT","USDT"]
telegram_conf = "/home/pi/workspace/telegram/confs/channel_gmt_usdt.conf"
duration = "60 minutes ago UTC"
client = Client(api_key, api_secret)
interval = Client.KLINE_INTERVAL_1MINUTE
pwd = "/home/pi/workspace/binance/binanceNewsScrapper/"

# Get data
klines = client.get_historical_klines(f"{pairs[0]}{pairs[1]}", interval, duration)

# Adapting data
columns_values = [
          "Date",
          "Open",
          "High",
          "Low",
          "Close",
          "Volume",
          "Close time",
          "Quote asset volume",
          "Number of trades",
          "Taker buy base asset volume",
          "Taker buy quote asset volume",
          "Ignore"
]
klines_df = pd.DataFrame(klines, columns =columns_values)
cf.set_config_file(theme='henanigans',sharing='public',offline=True)

now = datetime.now()
str_now = now.strftime('%H:%M:%S')
qf=cf.QuantFig(klines_df,title=f"Last hour | captured at {str_now}",legend='top',name=f'{pairs[0]}/{pairs[1]}')

fugg = qf.figure()
image_path = f"{pwd}images/gmt_usdt_{now.strftime('%Y-%m-%d')}_{str_now.replace(':','_')}.png"
fugg.write_image(image_path)
with open(image_path,"rb") as image_f:
    telegram_send.send(images=[image_f],conf=telegram_conf)
