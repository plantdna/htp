import pandas as pd
import os


def generate_df(df_a, df_b):
    new_file_data = []
    for index_a, row_a in df_a.iterrows():
        for index_b, row_b in df_b.iterrows():
            new_row = []
            for i in range(len(row_a)):
                item_value = [row_a[i], row_b[i]]
                item_value.sort()
                new_row.append('/'.join([str(v) for v in item_value]))
            new_file_data.append(new_row)
    new_df = pd.DataFrame(new_file_data, columns=df_a.columns.tolist())
    return new_df
 


def hpb(params):
    ROOT_DIR = params['ROOT_DIR']
    zayou_raw_path = params['input_path']
    output_path = params['output_path']

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_names = [name for name in os.listdir(zayou_raw_path) if (name[0] != '.' and name[-4:] == '.csv')]
    
    # 统计每个群的单体型情况
    htp_block_df = pd.read_csv('{}/dataset/haplotype_database.csv'.format(ROOT_DIR))
    htp_block_df = htp_block_df[['Haplotype Index','Chr','HTP ID']].copy()
    group_names = [name for name in os.listdir(zayou_raw_path) if name[-4:] == '.csv']
    for name in group_names:
        htp_block_df[name] = 0

    htp_block_df.set_index(['Haplotype Index', 'HTP ID'], inplace=True)

    for group_name in group_names:
        group_df = pd.read_csv('{}/{}'.format(zayou_raw_path, group_name))
        cols = group_df.columns.tolist()[1:]
        for col in cols:
            col_values = [v for v in list(set(group_df[col].tolist())) if v != 0]
            if len(col_values) > 0:
                for v in col_values:
                    htp_block_df.at[(v, col), group_name] = 1   
    
    htp_block_df['sum'] = htp_block_df.apply(lambda x: sum(x.values[3:]), axis=1)
    htp_block_df.to_csv('{}/group_blocks.csv'.format(output_path), index=False, encoding='utf-8_sig')

    # 构建虚拟杂优模式
    for i in range(len(file_names)):
        file_a_df = pd.read_csv('{}/{}'.format(zayou_raw_path, file_names[i]))
        for j in range(i+1, len(file_names)):
            file_b_df = pd.read_csv('{}/{}'.format(zayou_raw_path, file_names[j]))
            res_df = generate_df(file_a_df, file_b_df)
            res_df.to_csv(
                '{}/{}_hpb_{}.csv'.format(output_path, file_names[i].split('.')[0], file_names[j].split('.')[0]),
                index=False,
                encoding='utf-8_sig'
            )

if __name__ == '__main__':
    hpb(params)