import pandas as pd
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

        return round(common_num/len(str1), 3)


def similar_rate(list1, list2, st):
    common_num = 0
    for i in range(len(list1)):
        str1 = list1[i]
        str2 = list2[i]
        if str_compare(str1, str2) >= st:
            common_num+=1

    return [len(list1)-common_num, round(common_num/len(list1), 3)]


def wghca(params):
    compare_file_path = params['compare_file_path']
    contrast_file_path = params['contrast_file_path']
    output_path = params['output_path']
    st = params['st']
    
    res_dataset = []

    file1_df = pd.read_csv(compare_file_path)
    file2_df = pd.read_csv(contrast_file_path)

    if file1_df.shape[1] == file2_df.shape[1]:
        file1_len = len(file1_df)
        file2_len = len(file2_df)

        for i in range(file1_len):
            for j in range(i+1, file2_len):
                file1_row = file1_df.loc[i].tolist()
                file2_row = file2_df.loc[j].tolist()
                compare_res = similar_rate(file1_row[1:], file2_row[1:], st)
                res_dataset.append([
                    file1_row[0],
                    file2_row[0],
                    compare_res[0],
                    compare_res[1],
                ])

        res_df = pd.DataFrame(res_dataset, columns=['Sam1', 'Sam2', 'Diff_Num', 'Similar_Rate'])
        base_class.append_write_csv_by_df(res_df, output_path, 'wghca_compare_result')
    
    else:
        raise RuntimeError('Both matrices should have the same number of columns')


if __name__ == '__main__':
    wghca(params)
