import pandas as pd
import time
import multiprocessing
import math

from scripts.base_class import BaseClass

base_class = BaseClass()

def str_compare(str1, str2):
    if len(str1) != len(str2):
        return 0
    else:
        common_num = 0
        for i in range(len(str1)):
            if str1[i] == str2[i]:
                common_num+=1
        if len(str1) <= 10:
            if common_num == len(str1):
                return round(common_num/len(str1), 3)
            else:
                return 0
        else:
            return round(common_num/len(str1), 3)


def similar_rate(list1, list2):
    common_num = 0
    for i in range(len(list1)):
        str1 = list1[i]
        str2 = list2[i]
        if str_compare(str1, str2) >= st:
            common_num+=1

    return [len(list1)-common_num, round(common_num/len(list1), 3)]

def write_compare_result(res_dataset):
    res_df = pd.DataFrame(res_dataset, columns=['Sam1', 'Sam2', 'Diff_Num', 'Similar_Rate'])
    base_class.append_write_csv_by_df(res_df, output_path, 'wghca_compare_result_{}'.format(timestamp))


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

def wghca(params):
    compare_file_path = params['compare_file_path']
    contrast_file_path = params['contrast_file_path']
    process_pool_num = int(params['process'])

    global st
    st = params['st']

    global output_path
    output_path = params['output_path']

    global timestamp
    timestamp = int(round(time.time() * 1000))


    file1_df = pd.read_csv(compare_file_path)
    file2_df = pd.read_csv(contrast_file_path)

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
    wghca(params)
