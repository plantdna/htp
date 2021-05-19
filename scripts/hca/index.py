import pandas as pd
import time

from scripts.base_class import BaseClass

base_class = BaseClass()

def similar_rate(list1, list2, missing_str):
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
    

def hca(params):
    res_dataset = []
    timestamp = int(round(time.time() * 1000))

    file_path_1 = params['compare_file_path']
    file_path_2 = params['contrast_file_path']
    output_path = params['output_path']
    missing_str = params['ms']

    file1_df = pd.read_csv(file_path_1)
    file2_df = pd.read_csv(file_path_2)

    if file1_df.shape[1] == file2_df.shape[1]:
        file1_len = len(file1_df)
        file2_len = len(file2_df)

        for i in range(file1_len):
            for j in range(i+1, file2_len):
                file1_row = file1_df.loc[i].tolist()
                file2_row = file2_df.loc[j].tolist()
                compare_res = similar_rate(file1_row[1:], file2_row[1:], missing_str)

                res_dataset.append([
                    file1_row[0],
                    file2_row[0],
                    compare_res[0],
                    compare_res[1],
                ])

        
        res_df = pd.DataFrame(res_dataset, columns=['Sam1', 'Sam2', 'Diff_Num', 'Similar_Rate'])
        base_class.append_write_csv_by_df(res_df, output_path, 'hca_compare_result_{}'.format(timestamp))

    else:
        raise RuntimeError('Both matrices should have the same number of columns')

if __name__ == '__main__':
    hca(params)
