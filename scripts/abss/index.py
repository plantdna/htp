from datetime import datetime
import sys
import traceback
import os
import pandas as pd

from utils.groupby_chr import groupby_chr
from utils.fitting import fitting
from utils.generate_dataset import generate_dataset
from utils.compare import compare
from utils.denoise import denoise
from utils.to_htp import to_htp
from utils.final_result import final_result
from utils.draw_image import draw_group


def abss(params):
    '''
    回交转育群体的背景回复分析
    '''
    try:
        # 定义文件路径
        output_path = params['output_path']
        board_dir = '{}/board_data'.format(output_path)
        chr_dir = '{}/chr_data'.format(output_path)
        dataset_dir = '{}/dataset'.format(output_path)
        compare_dir = '{}/compare'.format(output_path)
        chr_htp_dir = '{}/chr_htp'.format(output_path)
        denoise_snp_dir = '{}/denoise_snp'.format(output_path)
        denoise_htp_dir = '{}/denoise_htp'.format(output_path)
        final_dir = '{}/final_result'.format(output_path)
        images_dir = '{}/images'.format(output_path)

        genotyping_files_dir = params['genotype_files_dir']
        tracke_probeset_file_path = '{}/tracke_probeset.json'.format(output_path)

        # 检查输出路径
        print('检查输出路径')
        if os.path.exists(output_path):
            os.system('rm -rf {}'.format(output_path))

        # load dataset
        print('加载标记信息')
        probeset_info_df = pd.read_csv('../../dataset/marker_info.csv', low_memory=False)
        probeset_info_df.set_index('probeset_id', inplace=True)
        # load sample info excel
        print('加载样品信息表')
        sample_info_df = pd.read_excel(params['sample_file_path'])
        rp_call_codes = sample_info_df[sample_info_df['order'] == 0]['call_code'].tolist()
        dp_call_codes = sample_info_df[sample_info_df['order'] == 1]['call_code'].tolist()

        print('拆分合并基因型文件')
        groupby_chr(genotyping_files_dir, board_dir, 5, chr_dir)
        
        # 拟合供体数据，筛选跟踪标记
        print('拟合数据，确定跟踪标记')
        fitting(
            chr_dir,
            rp_call_codes,
            dp_call_codes,
            probeset_info_df,
            True,
            tracke_probeset_file_path,
            '{}/select_snp'.format(images_dir)
        )

        # 构建数据子集
        print('构建数据子集')
        sample_info_df.loc[len(sample_info_df)] = ['simulate_fitting_rp_by_rps', '', 0]
        sample_info_df.loc[len(sample_info_df)] = ['simulate_fitting_rp_by_group', '', 0]
        sample_info_df.loc[len(sample_info_df)] = ['simulate_fitting_dp_by_group', '', 0]

        generate_dataset(
            chr_dir, 
            dataset_dir,
            tracke_probeset_file_path, 
            sample_info_df
        )

        # 群体与受体比对
        print('数据比对')
        compare(
            dataset_dir, 
            compare_dir,
            'simulate_fitting_rp_by_rps'
        )

        # SNP结果降噪
        print('SNP数据降噪')
        denoise(compare_dir, denoise_snp_dir)

        # SNP TO HTP
        print('转换成HTP')
        to_htp(denoise_snp_dir, chr_htp_dir, probeset_info_df)

        # HTP结果降噪
        print('HTP结果降噪')
        denoise(chr_htp_dir, denoise_htp_dir)

        # 统计
        print('结果统计')
        final_result(
            denoise_snp_dir, 
            denoise_htp_dir, 
            final_dir,
        )

        # 绘制BC群体的回复情况图
        print('draw image')
        draw_group(denoise_htp_dir, '{}/bc_images'.format(images_dir))



    except Exception as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_exception(
            exc_type,
            exc_value,
            exc_traceback_obj
        )


if __name__ == '__main__':
    abss(params)
