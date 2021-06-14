# CLTV = (Customer_Value / Churn_Rate) x Profit_margin.
# Customer_Value = Average_Order_Value * Purchase_Frequency
# Average_Order_Value = Total_Revenue / Total_Number_of_Orders
# Purchase_Frequency =  Total_Number_of_Orders / Total_Number_of_Customers
# Churn_Rate = 1 - Repeat_Rate
# Profit_margin

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.width', 700)

# Reading data.
df_ = pd.read_excel("Week_03/datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()
df.head()

# Data preprocessing.
df = df[~df["Invoice"].str.contains("C", na=False)]
df = df[(df['Quantity'] > 0)]
df.dropna(inplace=True)
df["TotalPrice"] = df["Quantity"] * df["Price"]

# Creating cltv_df dataframe with CLTV parameters.
cltv_df = df.groupby('Customer ID').agg({'Invoice': lambda x: len(x),
                                         'Quantity': lambda x: x.sum(),
                                         'TotalPrice': lambda x: x.sum()})

cltv_df.columns = ['total_transaction', 'total_unit', 'total_price']

cltv_df.head()

# Calculate average order value.
cltv_df['avg_order_value'] = cltv_df['total_price'] / cltv_df['total_transaction']

# Calculate Purchase Frequency
cltv_df["purchase_frequency"] = cltv_df['total_transaction'] / cltv_df.shape[0]

# Calculate Repeat Rate and Churn Rate
repeat_rate = cltv_df[cltv_df.total_transaction > 1].shape[0] / cltv_df.shape[0]
churn_rate = 1 - repeat_rate

#  Calculate Profit
cltv_df['profit'] = cltv_df['total_price'] * 0.05

# Calculate Customer Lifetime Value
cltv_df['CV'] = (cltv_df['avg_order_value'] * cltv_df["purchase_frequency"]) / churn_rate

cltv_df['CLTV'] = cltv_df['CV'] * cltv_df['profit']

cltv_df.sort_values("CLTV", ascending=False)

# Scaling values
scaler = MinMaxScaler(feature_range=(1, 100))
scaler.fit(cltv_df[["CLTV"]])
cltv_df["SCALED_CLTV"] = scaler.transform(cltv_df[["CLTV"]])

cltv_df.sort_values("CLTV", ascending=False)

cltv_df[["total_transaction", "total_unit", "total_price", "CLTV", "SCALED_CLTV"]].sort_values(by="SCALED_CLTV",
                                                                                               ascending=False).head()

cltv_df.sort_values("total_price", ascending=False)

cltv_df["segment"] = pd.qcut(cltv_df["SCALED_CLTV"], 4, labels=["D", "C", "B", "A"])

cltv_df[["segment", "total_transaction", "total_unit", "total_price", "CLTV", "SCALED_CLTV"]].sort_values(
    by="SCALED_CLTV",
    ascending=False).head()

cltv_df.groupby("segment")[["total_transaction", "total_unit", "total_price", "CLTV", "SCALED_CLTV"]].agg(
    {"count", "mean", "sum"})



