import pandas as pd
import traceback
from scripts.base_class import BaseClass

base_class = BaseClass()

def generator_htp_sequence(params):
    try:
        step1_dir_path = params['data_path']
        output_path = params['output_path']
        ROOT_DIR = params['ROOT_DIR']

        # load htp and snp mapping file
        marker_info_df = pd.read_csv('{}/dataset/marker_info.csv'.format(ROOT_DIR))
        chr_marker_info_group = marker_info_df.groupby(by='chr')
        
        # group by chr
        for chr_id, chr_marker_df in chr_marker_info_group:
            chr_htp_seq_df = []

            chr_df = pd.read_csv('{}/chr{}.csv'.format(step1_dir_path, chr_id))
            chr_samples = chr_df.columns.values.tolist()[4:]

            # group by chr htp
            chr_htp_group = chr_marker_df.groupby(by='HTP')
            for htp, htp_df in chr_htp_group:
                htp_probesets = htp_df['probeset_id'].tolist()
                chr_htp_df = chr_df[chr_df['probeset_id'].isin(htp_probesets)][chr_samples].T.reset_index()
                htp_seq_array = []
                for index, row in chr_htp_df.iterrows():
                    row_list = row.tolist()
                    row_Index = row_list[0]
                    row_geno_list = row_list[1:]
                    seq_a = ''
                    seq_b = ''
                    for geno in row_geno_list:
                        if geno == '---':
                            seq_a += '-'
                            seq_b += '-'
                        else:
                            seq_a += geno.split('/')[0]
                            seq_b += geno.split('/')[-1]

                    htp_seq_array.append([
                        row_Index,
                        '{}/{}'.format(seq_a, seq_b)
                    ])
                
                htp_seq_df = pd.DataFrame(htp_seq_array, columns=['Index', htp])
                if len(chr_htp_seq_df) == 0:
                    chr_htp_seq_df = htp_seq_df
                else:
                    chr_htp_seq_df = pd.merge(chr_htp_seq_df, htp_seq_df, on='Index')

            base_class.append_write_csv_by_df(chr_htp_seq_df, output_path, 'chr{}'.format(chr_id))
        return 

    except Exception as e:
        traceback.print_exc()

if __name__ == '__main__':
    generator_htp_sequence(params)