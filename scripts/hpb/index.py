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
    zayou_raw_path = params['input_path']
    output_path = params['output_path']

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_names = [name for name in os.listdir(zayou_raw_path) if (name[0] != '.' and name[-4:] == '.csv')]

    for i in range(len(file_names)):
        file_a_df = pd.read_csv('{}/{}'.format(zayou_raw_path, file_names[i]))
        for j in range(i+1, len(file_names)):
            file_b_df = pd.read_csv('{}/{}'.format(zayou_raw_path, file_names[j]))
            res_df = generate_df(file_a_df, file_b_df)
            res_df.to_csv(
                '{}/{}_{}.csv'.format(output_path, file_names[i].split('.')[0], file_names[j].split('.')[0]),
                index=False,
                encoding='utf-8_sig'
            )

if __name__ == '__main__':
    hpb(params)