
from os import PRIO_USER
import pandas as pd
import numpy as np
import time

lcfs = []

def format_parent(df):
    new_df = df.copy()
    new_df['smooth'] = ''
    for index, row in df.iterrows():
        if not row['parent']:
            new_df.at[index, 'smooth'] = 'x'
        else:
            parents = row['parent'].split(',')
            if len(parents) == 1:
                pass
            else:
                new_df.at[index, 'smooth'] = 'x'

    return new_df


def findLCF(df):
    '''
    找出lcf
    :return:
    '''
    blockIndex = None
    for index, row in df.iterrows():
        if row['smooth'] != 'x':
            if index+1 < len(df):
                if df.iloc[index+1]['smooth'] != 'x':
                    blockIndex = index
                    blockDf = df.iloc[:index]
                    lcfs.append(blockDf[blockDf['smooth']=='x']['col'].tolist())
                    newDf = df.iloc[index+2:].copy()
                    newDf.reset_index(inplace=True)
                    newDf.drop('index', axis=1, inplace=True)
                    return findLCF(newDf)
                    break
    if not blockIndex:
        lcfs.append(df[df['smooth'] == 'x']['col'].tolist())
    


def find_parent(col, df):
    first_col = df.columns.tolist()[0]
    parents = []
    children = df.loc[0][col]
    for i in range(len(df)-1):
        if df.loc[i+1][col] == children:
            parents.append(str(df.loc[i+1][first_col]))

    return ','.join(parents)


def ilpa(params):
    '''
    默认第一行为需要推测inbredx的数据
    '''
    input_path = params['input_path']
    output_path = params['output_path']
    file_df  = pd.read_csv(input_path)
    columns = file_df.columns.tolist()
    first_col = columns[0]

    compare_df = pd.DataFrame({'col': columns[1:]})
    compare_df['parent'] = compare_df.apply(lambda x: find_parent(x['col'], file_df[[first_col, x['col']]]), axis=1)
    
    f_df = format_parent(compare_df)
    findLCF(f_df)
    lcf_lens = [len(lcf) for lcf in lcfs]
    max_len_index = lcf_lens.index(max(lcf_lens))
    lcf = lcfs[max_len_index]
    
    inbredX_df = file_df.iloc[:1][[first_col]+lcf]
    inbredX_df.to_csv('{}/inbredX_{}.csv'.format(output_path, int(round(time.time() * 1000))), index=False, encoding='utf-8_sig')


if __name__ == '__main__':
    ilpa()