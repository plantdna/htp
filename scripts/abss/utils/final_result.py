import os
from .base import color_excel, statistics

def final_result(snp_files_path, htp_files_path, output_path):
    '''
    给结果着色
    '''
    if os.path.exists(output_path):
        os.system('rm -rf {}'.format(output_path))

    for chr_id in range(1, 11):
        color_excel('{}/chr{}.csv'.format(snp_files_path, chr_id), output_path, 'chr{}_SNP'.format(chr_id), 2)
        color_excel('{}/chr{}.csv'.format(htp_files_path, chr_id), output_path, 'chr{}_HTP'.format(chr_id), 2)

    statistics(snp_files_path, htp_files_path, output_path)

