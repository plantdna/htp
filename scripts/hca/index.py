import pandas as pd
import time
import multiprocessing
import math

from scripts.base_class import BaseClass

base_class = BaseClass()

def similar_rate(list1, list2):
    common_num = 0
    missing_num = 0
    for i in range(len(list1)):
        if list1[i] == list2[i]:
            common_num+=1
        if list1[i] == missing_str or list2[i] == missing_str:
            missing_num += 1

    if (len(list1)-missing_num) == 0:
        return [0, 0]
    else:
        return [len(list1)-missing_num-common_num, round(common_num/(len(list1)-missing_num), 3)]
    

def write_compare_result(res_dataset):
    res_df = pd.DataFrame(res_dataset, columns=['Sam1', 'Sam2', 'Diff_Num', 'Similar_Rate'])
    base_class.append_write_csv_by_df(res_df, output_path, 'hca_compare_result_{}'.format(timestamp))


def compare(df1, df2):
    res_dataset = []
    for index_a, row_a in df1.iterrows():
        for index_b, row_b in df2.iterrows():
            row_a_list = row_a.tolist()
            row_b_list = row_b.tolist()
            print(row_a_list[0], row_b_list[0])
            compare_res = similar_rate(row_a_list[1:], row_b_list[1:])
            res_dataset.append([
                row_a_list[0],
                row_b_list[0],
                compare_res[0],
                compare_res[1],
            ])

    return res_dataset


def hca(params):
    global timestamp
    timestamp = int(round(time.time() * 1000))

    file_path_1 = params['compare_file_path']
    file_path_2 = params['contrast_file_path']

    global output_path
    output_path = params['output_path']

    global missing_str
    missing_str = params['ms']

    process_pool_num = int(params['process'])

    file1_df = pd.read_csv(file_path_1)
    file2_df = pd.read_csv(file_path_2)

    if file1_df.shape[1] == file2_df.shape[1]:
        pool = multiprocessing.Pool(process_pool_num)
        piece_num = math.ceil(len(file1_df)/process_pool_num)

        for piece in range(process_pool_num):
            if piece == 0:
                slice_df = file1_df.loc[0:(piece+1)*piece_num]
            else:
                slice_df = file1_df.loc[piece*piece_num+1:(piece+1)*piece_num]

            pool.apply_async(func=compare, args=(slice_df, file2_df,), callback=write_compare_result)

        pool.close()
        pool.join()

    else:
        raise RuntimeError('Both matrices should have the same number of columns')

if __name__ == '__main__':
    hca(params)
