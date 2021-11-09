import pandas as pd
import os
import json

from .base import append_write_csv_by_df

def generate_dataset(input_path, output_path, tracke_probeset_file_path, sample_info_df):
    '''
    根据差异标记和参与比对的样品编号生成新的数据集
    '''

    if os.path.exists(output_path):
        os.system('rm -rf {}'.format(output_path))

    f = open(tracke_probeset_file_path,'r',encoding='utf-8')
    chr_probesets = json.load(f)
    f.close()

    # 获取需要比对的样品
    compare_codes = sample_info_df['call_code'].tolist()
    code_orders = {}
    code_names = {}

    for index, row in sample_info_df.iterrows():
        code_orders[row['call_code']] = row['order']
        code_names[row['call_code']] = row['sample_name']


    for key in chr_probesets:
        chr_df = pd.read_csv('{}/{}.csv'.format(input_path, key))
        new_chr_df = chr_df[['call_code']+chr_probesets[key]]
        new_chr_df.insert(1, 'sample_name', '')

        new_chr_df = new_chr_df[new_chr_df['call_code'].isin(compare_codes)].copy()
        new_chr_df['order'] = new_chr_df[['call_code']].apply(lambda x: code_orders[x['call_code']], axis=1)
        new_chr_df['sample_name'] = new_chr_df[['call_code']].apply(lambda x: code_names[x['call_code']], axis=1)
        new_chr_df.sort_values(by='order', ascending=True, inplace=True)
        new_chr_df.drop(['order'], axis=1, inplace=True)
        append_write_csv_by_df(new_chr_df, output_path, key)

    
