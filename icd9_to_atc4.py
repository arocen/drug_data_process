# 对于china_trial每行数据，根据icd9匹配atc-4

import os
import pandas as pd

from dotenv import load_dotenv

load_dotenv() # load .env file


# To-do: change these environment variables accordingly
column_name_of_icd9 = os.environ.get("column_name_of_icd9")
index_of_atc4_column = os.environ.get("index_of_atc_column")   # index start with 1
output_save_path = os.environ.get("output_save_path")
input_data_path = os.environ.get("input_data_path")
ICD2ATC_path = os.environ.get("ICD2ATC_path")

def icd9_to_atc4(icd9:str, ICD2ATC_df:pd.DataFrame)->str:
    '''input icd9 value, return atc-4 accordingly'''
    # To-do: 补充这个函数
    atc4_distr = ICD2ATC_df[lambda ICD2ATC_df: ICD2ATC_df["ICD"] == icd9]
    print(atc4_distr)
    return


def read_ICD2ATC(path:str=ICD2ATC_path)->pd.DataFrame:
    '''read ICD2ATC excel file'''

    dtypes = {
        "ATC": "category", 
        "ICD": "category",
        "Prob": "float"
    }

    df = pd.read_excel(path, dtype=dtypes)
    return df


def iterate_over(icd9_df:pd.DataFrame, ICD2ATC_df:pd.DataFrame)->pd.DataFrame:
    '''
    遍历dataframe每一行, 返回写入atc-4后的dataframe
    设置缺失值处理逻辑
    '''
    
    for i in range(1, len(icd9_df) + 1):
        icd9 = icd9_df.columns.get_loc(column_name_of_icd9)

        # 设置缺失值判别条件
        if icd9 != None:
            # 调用helper function，将atc-4写入该列
            icd9_df.iat[i - 1, index_of_atc4_column] = icd9_to_atc4(icd9)    # increase efficiency by using df.iat
        else:
            # 跳过缺失值的处理
            continue

    return icd9_df



def test_icd9_to_atc4():
    icd9 = "8"
    ICD2ATC_df = read_ICD2ATC()
    print(ICD2ATC_df)
    icd9_to_atc4(icd9, ICD2ATC_df)

# test icd9_to_atc4 function
test_icd9_to_atc4()


# def main():
#     # 用pandas读取indication > icd9操作后的结果，成为dataframe对象
#     icd9_df = pd.read_excel(input_data_path)

#     # 插入新的一列用于存储atc-4 value
#     # icd9_df['atc-4'] = None # 通过事先手动插入来注释掉这一行
    
#     # 读取包含ICD到ATC转换关系的excel
#     ICD2ATC_df = read_ICD2ATC()

#     # 遍历每一行, 处理得到写入atc-4的dataframe对象
#     df = iterate_over(icd9_df, ICD2ATC_df)

#     # 用pandas将dataframe对象保存为新的excel文件
#     df.to_excel(output_save_path)


# if __name__ == "__main__":
#     main()