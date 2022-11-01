import pandas as pd
from binance.client import Client
import datetime
from datetime import timezone
import asyncio
from binance import BinanceSocketManager
from config import api_secret, api_key


client1 = Client(api_key, api_secret)
bsm = BinanceSocketManager(client1)

sym = "1000SHIBUSDT"
socket = bsm.symbol_mark_price_socket(sym)
balance = 90


def mrk_price_df(msg):

    df = pd.DataFrame([msg['data']])

    df = df.loc[:, ['s', 'E', 'p', 'r', 'T']]
    df.columns = ['symbol', 'Time', 'Price', 'funding', 'nextfunding']
    df.Price = df.Price.astype(float)
    df.funding = df.funding.astype(float)
    df.Time = df.Time.astype('string')
    df.nextfunding = df.nextfunding.astype('string')

    print(df)
    return df


async def main():
    while True:

        await socket.__aenter__()
        msg = await socket.recv()
        df = mrk_price_df(msg)

        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = int(utc_time.timestamp())

        if len(df['nextfunding'].iloc[-1]) != len(str(utc_timestamp)):
            utc_timestamp = str(utc_timestamp) + "0"*(len(df['nextfunding'].iloc[-1]) - len(str(utc_timestamp)))
            utc_timestamp = int(utc_timestamp)

        amt1 = balance

        if int(df['nextfunding'].iloc[-1]) == utc_timestamp:

            client1.futures_create_order(symbol=sym, side="BUY", type='MARKET',quantity=amt1)
            print(f"Time of funding{utc_timestamp}, total amount: {amt1}")

            await asyncio.sleep(2)

            client1.futures_create_order(symbol=sym, side="SELL", type='MARKET', quantity=amt1)

            break

        else:
            print(f"Time remaining : {(int(df['nextfunding'].iloc[-1]) - utc_timestamp)/1000} seconds")



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())