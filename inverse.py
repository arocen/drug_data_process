# 由ATC-4 -> ICD-9对应关系求ICD-9 -> ATC-4关系

import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv() # load .env file

ATC2ICD_path = os.environ.get("ATC2ICD_path")
ICD2ATC_path = os.environ.get("ICD2ATC_path")

def read(original_path=ATC2ICD_path)->pd.DataFrame:
    '''
    read all sheets into one dataframe
    return pd.DataFrame
    '''

    dtypes = {
        "ATC": "category",
        "ICD": "category",
        "Prob": "float"
    }

    # Initialize an empty list to store DataFrames for each sheet
    dfs = []

    # Open the Excel file
    with pd.ExcelFile(original_path) as xls:
        # Get the list of sheet names
        sheet_names = xls.sheet_names

        # Iterate through each sheet
        for sheet_name in sheet_names:
            # Read the specific columns from the current sheet
            df = pd.read_excel(xls, sheet_name, dtype=dtypes, usecols=list(dtypes))

            # Append the DataFrame to the list
            dfs.append(df)

    # Concatenate all DataFrames into one
    result = pd.concat(dfs, ignore_index=True)

    

    # convert dtype into category
    result['ATC'] = result['ATC'].astype('category')
    result['ICD'] = result['ICD'].astype('category')
    print(result.dtypes)

    # check the data loaded
    print(result.head())
    print(len(result))
    return result



def transfer(original_df)->dict:
    '''Transfer the ATC-4 -> ICD-9 into ICD-9 -> ATC-4 relationshipss'''

    # 遍历, 计算逆向概率
    # 假设ATC-4的先验分布服从均匀分布, 平均计算不同年龄段和不同性别条件下的概率

    # 对于ICD-9的每一个取值, 获取对应的ATC4取值和概率, 对概率求和
    group_df = original_df.groupby(["ICD", "ATC"]).sum()

    # 对概率取均值，分母为所有表的数量
    # group_df["Prob"] = group_df["Prob"] / 8 # 归一化以后跟不除的结果是一样的

    # 归一化
    group_df["Prob"] = group_df["Prob"] / original_df.groupby(["ICD"]).sum(numeric_only=True)["Prob"]
    
    # 去除概率为0.0的行
    group_df = group_df[group_df["Prob"] != 0.00]
    print(group_df)

    # 存储为excel
    group_df.to_excel(ICD2ATC_path)
    return

# test
original_df = read()
transfer(original_df)