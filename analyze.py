#!/usr/bin/python3

import pandas as pd

df = pd.read_csv('yxny_5min.csv')

df['ewm_volume'] = df['volume'].ewm(span=48*15,min_periods=0,adjust=False,ignore_na=False).mean()
df['slot_in_day'] = df.index % 48

processed = df[df['volume'] > 2 * df['ewm_volume']]

processed.to_csv("yxny_processed.csv", index=False)

