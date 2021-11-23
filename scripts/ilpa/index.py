
# 根据上一步的比对结果,从结果文件中根据离群值取出符合条件的Bin.
import pandas as pd
import numpy as np

def continue_finder(start, compare_df, lens):
    for i in range(start, lens):
        if compare_df.loc[i]['parent'] == []:
            return continue_finder(i+1)
        else:
            return i


def find_parent(col, df):
    first_col = df.columns.tolist()[0]
    parents = []
    children = df.loc[0][col]
    for i in range(len(df)-1):
        if df.loc[i+1][col] == children:
            parents.append(str(df.loc[i+1][first_col]))

    return ','.join(parents)


def ilpa(params):
    '''
    默认第一行为需要推测inbredx的数据
    '''
    input_path = params['input_path']
    output_path = params['output_path']
    file_df  = pd.read_csv(input_path)
    columns = file_df.columns.tolist()
    first_col = columns[0]

    compare_df = pd.DataFrame({'col': columns[1:]})
    compare_df['parent'] = compare_df.apply(lambda x: find_parent(x['col'], file_df[[first_col, x['col']]]), axis=1)

    cols = columns[1:]
    # 统计X
    boxs = []
    box_lens = []
    lens = len(compare_df)

    for i in range(lens):
        next_i = continue_finder(i, compare_df, lens)
        if next_i != i:
            boxs.append(cols[i:next_i])
            box_lens.append(next_i-i)
            i = next_i

    percentile = np.percentile(box_lens, (25,75))
    iqr = percentile[1]-percentile[0]
    up_limit = percentile[1]+1.5*iqr
    target_bins = []
    for i in range(len(box_lens)):
        if box_lens[i] >= up_limit:
            target_bins+=boxs[i]

    inbredX_df = file_df.iloc[:1][[first_col]+target_bins]
    inbredX_df.to_csv('{}/inbredX.csv'.format(output_path), index=False, encoding='utf-8_sig')


if __name__ == '__main__':
    ilpa()