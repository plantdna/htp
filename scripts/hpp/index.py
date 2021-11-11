import traceback
import pandas as pd
import multiprocessing
import math
import os

from scripts.base_class import BaseClass

base_class = BaseClass()


def write_compare_result(params):
    for row in params['compare_result']:
        base_class.append_write_csv_by_list(row, params['output_path'], 'hmp_compare_result')


def compare(hybrid_df, output_path, group_dataset_path):
    htp_counts = len(hybrid_df.columns.values.tolist()[1:])
    group_names = [file_name for file_name in os.listdir(group_dataset_path) if file_name[-4:] == '.csv']

    compare_result = []
    for index_sample, sample_row in hybrid_df.iterrows():
        hybrid_genotype_list = sample_row.tolist()[1:]

        for group_name in group_names:
            max_similar_rate = 0
            file_reader = pd.read_csv('{}/{}'.format(group_dataset_path, group_name), sep=',', header=None, iterator=True)
            loop = True
            while loop:
                try:
                    chunk = file_reader.get_chunk(100)
                    for index, row in chunk.iterrows():
                        row_genotype_list = row.tolist()[1:]
                        similar_onps=0
                        for i in range(htp_counts):
                            parent_allele = str(row_genotype_list[i]).split('/')
                            children_allele = str(hybrid_genotype_list[i]).split('/')
                            if children_allele[0] in parent_allele and children_allele[1] in parent_allele:
                                similar_onps+=1
                        
                        similar_rate = round(similar_onps/htp_counts,3)
                        if similar_rate > max_similar_rate:
                            max_similar_rate = similar_rate

                except StopIteration:
                    loop = False

            compare_result.append([
                str(sample_row[0]),
                group_name[:-4],
                str(max_similar_rate)
            ])

    return {
        'compare_result': compare_result,
        'output_path': output_path,
    }


def main(params):
    try:
        hybrid_file_path = params['input_path']
        group_dataset_path = params['group_dataset_dir']
        output_path = params['output_path']


        process_pool_num = multiprocessing.cpu_count() - 1
        hybrid_onp_df = pd.read_csv(hybrid_file_path)

        base_class.append_write_csv_by_list(['ID', 'GROUP', 'MAX_SIMILARITY'], output_path, 'hmp_compare_result.csv')

        pool = multiprocessing.Pool(process_pool_num)
        piece_num = math.ceil(len(hybrid_onp_df)/process_pool_num)

        for piece in range(process_pool_num):
            if piece == 0:
                sample_slice_df = hybrid_onp_df.loc[0:(piece+1)*piece_num]
            else:
                sample_slice_df = hybrid_onp_df.loc[piece*piece_num+1:(piece+1)*piece_num]

            pool.apply_async(func=compare, args=(sample_slice_df,output_path,group_dataset_path,), callback=write_compare_result)

        pool.close()
        pool.join()

    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    main(params)
