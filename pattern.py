from pdb import pm
from pybit import HTTP
import pandas as pd
import time 
import datetime
import matplotlib.pyplot as plt

now = datetime.datetime.now()
today = datetime.datetime(
    year=now.year,
    month=now.month,
    day=now.day,
    hour=0,
    minute=0,
    second=0
)
delta = datetime.timedelta(days=-200)
dt = today + delta 
from_time = time.mktime(dt.timetuple())

session = HTTP(
    endpoint="https://api.bybit.com", 
    spot=False
)

resp = session.query_kline(
    symbol="BTCUSDT",
    interval="D",
    limit=200,
    from_time=from_time
)

result = resp['result']
df = pd.DataFrame(result)
ts = pd.to_datetime(df['open_time'], unit='s')
df.set_index(ts, inplace=True)
df = df[['open', 'high', 'low', 'close']]

change = ((df['close']-df['open'])/df['open'])*100


# 변화율에대한 정규화
data = [ ] #main
for i in change.tolist():
    if i >= 20: #20% 이상
        data.append(4)
    elif 10 <= i < 20: # 10이상 20미만 
        data.append(3)
    elif 5 <= i < 10: #5이상 10 미만
        data.append(2)
    elif 1 < i < 5: # #1초과 5 미만
        data.append(1)
    elif -1 <= i <= 1: #-1이상 1이하
        data.append(0)
    elif -5 < i < -1: # -5이상 -1이하
        data.append(-1)
    elif -10 < i <= -5: #-10 초과 -5 이하
        data.append(-2)
    elif -20 < i <= -10: # -20초과 -10이하
        data.append(-3)
    elif i <= -20: #-20 이하
        data.append(-4)
    else:
        print("Error") 

#사건하나에대한 확률
p4 = data.count(4)/200
p3 = data.count(3)/200
p2 = data.count(2)/200
p1 = data.count(1)/200
p0 = data.count(0)/200
pm1 = data.count(-1)/200
pm2 = data.count(-2)/200
pm3 = data.count(-3)/200
pm4 = data.count(-4)/200


df = data[data.index(data[-1]):]
#어제의 사건에대한 조건부확률
print(df.count(4)/len(df))
print(df.count(3)/len(df))
print(df.count(2)/len(df))
print(df.count(1)/len(df))
print(df.count(0)/len(df))
print(df.count(-1)/len(df))
print(df.count(-2)/len(df))
print(df.count(-3)/len(df))
print(df.count(-4)/len(df))
