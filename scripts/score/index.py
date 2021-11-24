import pandas as pd
import numpy as np
import os

def get_score(genotyoe, collection):
    alleles = [int(v) for v in genotyoe.split('/') if v != 0] if '/' in genotyoe else []
    score = 0
    if len(alleles) > 0:
        for allele in alleles:
            if allele in collection:
                score+=0.5
    return score
    

def score(params):
    groups_path = params['groups_path']
    output_path = params['output_path']

    groups_names = [name for name in os.listdir(groups_path) if (name[0] != '.' and name[-4:] == '.csv' and name != 'group_blocks.csv')]

    block_df = pd.read_csv('{}/group_blocks.csv'.format(groups_path))

    for filename in groups_names:
        group_df = pd.read_csv('{}/{}'.format(groups_path, filename))        
        groups = filename[:-4].split('_hpb_')
        if groups[0] != groups[1]:
            select_df = block_df[
                ((block_df[groups[0]]==1) & (block_df[groups[1]]==1) & (block_df['sum']==2)) | ((block_df[groups[0]]==1) & (block_df['sum']==1)) |((block_df[groups[1]]==1) & (block_df['sum']==1))
            ].copy()
        else:
            select_df = block_df[
                (block_df[groups[0]]==1) & (block_df['sum']==1)
            ].copy()
        
        select_htps = list(set(select_df['HTP ID'].tolist()))
        select_htp_index_map = {}
        for htp in select_htps:
            select_htp_index_map[htp] = select_df[select_df['HTP ID'] == htp]['Haplotype Index'].tolist()

        new_df = group_df[['call_code']+select_htps].copy()    

        sample_score = []

        for index, row in new_df.iterrows():
            score = 0
            for key, value in select_htp_index_map.items():
                score+=get_score(row[key], value)

            sample_score.append([row['call_code'], round(score/len(select_htp_index_map), 8)])

        sample_score_df = pd.DataFrame(sample_score, columns=['call_code', 'score'])
        sample_score_df.to_csv('{}/{}_score.csv'.format(output_path, filename[:-4]), index=False, encoding='utf-8_sig')

        print('score is:', np.mean(sample_score_df['score'])+3*np.std(sample_score_df['score']))


if __name__ == '__main__':
    score(params)