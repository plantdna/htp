import pandas as pd
import traceback
from scripts.base_class import BaseClass

base_class = BaseClass()

def match_haplotype(seq, htp_haplotype_df):
    '''
    找出与指定序列相似度最高的单体型序号
    '''
    max_similar_index = 0
    max_rate = 0
    for index, row in htp_haplotype_df.iterrows():
        rate = base_class.similar_rate(seq, row['Haplotype Sequence'])
        if rate > max_rate:
            max_rate = rate
            max_similar_index = row['Haplotype Index']

    return max_similar_index


def generator_htp_index(params):
    try:
        step2_dir_path = params['data_path']
        output_path = params['output_path']
        htp_file_path = params['htp_file_path']
        ROOT_DIR = params['ROOT_DIR']

        haplotype_df = pd.read_csv('{}/dataset/haplotype_database.csv'.format(ROOT_DIR))
        htp_df = []

        for chr_id in range(1, 11):
            chr_df = pd.read_csv('{}/chr{}.csv'.format(step2_dir_path, chr_id))
            chr_htps = chr_df.columns.values.tolist()[1:]

            for index, row in chr_df.iterrows():
                for htp in chr_htps:
                    htp_haplotype_df = haplotype_df[haplotype_df['HTP ID'] == htp]
                    htp_allele = row[htp].split('/')
                    if htp_allele[0] == htp_allele[-1]:
                        haplotype_index = match_haplotype(htp_allele[0], htp_haplotype_df)
                        chr_df.loc[index, htp] = '{}/{}'.format(haplotype_index, haplotype_index)
                    else:
                        chr_df.loc[index, htp] = '{}/{}'.format(
                            match_haplotype(htp_allele[0], htp_haplotype_df),
                            match_haplotype(htp_allele[-1], htp_haplotype_df),
                        )

            if len(htp_df) == 0:
                htp_df = chr_df
            else:
                htp_df = pd.merge(htp_df, chr_df, on='Index')
            base_class.append_write_csv_by_df(chr_df, output_path, 'chr{}'.format(chr_id))
        
        base_class.append_write_csv_by_df(htp_df, htp_file_path, 'all_htps')
        return 
        
    except Exception as e:
        traceback.print_exc()

if __name__ == '__main__':
    generator_htp_index(params)