import pandas as pd

'''
构建单体型列表
'''
htp_block_df = pd.read_csv('../files/htp/bin_blocks_2021-08-01.csv')
htp_block_df.drop(['Sequence','Rate'], inplace=True, axis=1)
group_names = [name.split('.')[0] for name in os.listdir('../files/htp/zayou_2021-09-25') if name[0] != '.']
for name in group_names:
    htp_block_df[name] = 0

htp_block_df.set_index(['Index', 'HTP ID'], inplace=True)

for group_name in group_names:
    group_df = pd.read_csv('../files/htp/zayou_2021-09-25/{}.csv'.format(group_name))
    cols = group_df.columns.tolist()[1:]
    for col in cols:
        htp_id = 'HTP_{}'.format(col.split('Bin')[1])
        col_values = [v for v in list(set(group_df[col].tolist())) if v != 0]
        if len(col_values) > 0:
            for v in col_values:
                htp_block_df.at[(v, htp_id), group_name] = 1           
