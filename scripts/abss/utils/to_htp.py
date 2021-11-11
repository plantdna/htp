import pandas as pd
import os

from .base import snp2htp

def to_htp(input_path, output_path, htp_df):
    '''
    平滑后的结果转成HTP
    '''

    if os.path.exists(output_path):
        os.system('rm -rf {}'.format(output_path))

    for chr_id in range(1, 11):
        chr_htp_df = htp_df[htp_df['chr'].isin([chr_id, str(chr_id)])]
        snp2htp('{}/chr{}.csv'.format(input_path, chr_id), output_path, chr_id, chr_htp_df)

