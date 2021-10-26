#!/usr/bin/python3

import baostock as bs
import pandas as pd
import datetime

selected = {
        "sz.002594": "byd",
        "sz.000683": "yxny",
        "sz.003022": "lhxk",
        "sh.600111": "bfxt",
        "sh.600089": "tbdg"
}

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取沪深A股历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
# 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
today_str = datetime.date.today().strftime("%Y-%m-%d")
print(today_str)
for code, name in selected.items():
    rs = bs.query_history_k_data_plus(code,
        "date,code,open,high,low,close,volume,amount,adjustflag",
        start_date='2020-01-01',
        frequency="5", adjustflag="3")
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    result.to_csv(name + "_5min.csv", index=False)
    print(result)

    df = pd.read_csv(name + '_5min.csv')

    df['ewm_volume'] = df['volume'].ewm(span=48*15,min_periods=0,adjust=False,ignore_na=False).mean()
    df['slot_in_day'] = df.index % 48

    processed = df[df['volume'] > 2 * df['ewm_volume']]

    processed.to_csv(name + "_processed.csv", index=False)

#### 登出系统 ####
bs.logout()
