import pandas as pd
import os
import traceback
from scripts.base_class import BaseClass

'''
Step1 将genotyping 文件按染色体拆分
'''
base_class = BaseClass()

def handle_chr_df(dir_path):
    '''
    按染色体处理数据, 替换Indel基因分型
    '''
    for chr_id in range(1, 11):
        chr_df = pd.read_csv('{}/chr{}.csv'.format(dir_path, chr_id))
        samples = chr_df.columns.values.tolist()[4:]
        for index, row in chr_df.iterrows():
            if row['markertype'] == 'INDEL':
                for sample_name in samples:
                    chr_df.loc[index, sample_name] = base_class.format_indel_allele(chr_df.loc[index, sample_name])
        
        # 按位点位置排序
        chr_df.sort_values(by=['Start'], ascending=[True], inplace=True)
        chr_df.to_csv('{}/chr{}.csv'.format(dir_path, chr_id), index=False, encoding='utf-8_sig')
    return


def split_genotyping_file_by_chr(params):
    try:
        file_path = params['file_path']
        output_path = params['output_path']

        file_reader = pd.read_csv(file_path, skiprows=5, sep='\t', iterator=True)
        validate_cols = []
        # 循环读取基因数据
        loop= True
        while loop:
            try:
                chunk = file_reader.get_chunk(100)
                if len(validate_cols) == 0:
                    sample_names = [code for code in chunk.columns.tolist() if 'call_code' in code]
                    validate_cols = ['probeset_id', 'Start', 'Chr_id', 'markertype'] + sample_names

                filter_chunk = chunk[validate_cols].copy()
                filter_chunk['Chr_id'] = filter_chunk['Chr_id'].astype(str)

                filter_groups = filter_chunk.groupby(by="Chr_id")
                for chr_id, chr_df in filter_groups:
                    file_name = 'chr{}'.format(chr_id)
                    base_class.append_write_csv_by_df(chr_df, output_path, file_name)

            except StopIteration:
                loop = False
        
        handle_chr_df(output_path)

        return

    except Exception as e:
        traceback.print_exc()
    

if __name__ == '__main__':
    split_genotyping_file_by_chr(params)