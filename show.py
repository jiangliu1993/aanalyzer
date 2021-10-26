#!/usr/bin/python3

import finplot as fplt
import pandas as pd
df = pd.read_csv("processed.csv")

fplt.candlestick_ochl(df[['open', 'close', 'high', 'low']])
fplt.show()
