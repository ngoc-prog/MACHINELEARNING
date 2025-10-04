import pandas as pd

from basicdata.MyStatistic import MyStatistic

df=pd.read_csv("../dataset/SalesTransactions/SalesTransactions.csv",
               sep=',',encoding='utf-8',low_memory=False)

print(df)
print("="*50)
min_value=100
max_value=150
ms=MyStatistic()
df_filter=ms.find_orders_within_range(df,min_value,max_value)
print(df_filter)