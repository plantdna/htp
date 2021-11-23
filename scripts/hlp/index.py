import pandas as pd

def getNBayes(P_H):
    P_E_H = 1-0.01
    P_E_NH = 0.5
    P_HNew = P_H
    P_E = 0
    for i in range(10):
        P_E = P_E_H * P_HNew + P_E_NH *( 1 - P_HNew )
        P_HNew = P_E_H * P_HNew / P_E
    # end for
    return P_HNew, P_E


# end def

valid_str = ['A', 'T', 'C', 'G']

def get_similary(str1, str2):
    '''
    str1: 包含缺失
    str2: 无缺失
    '''
    min_len = min([len(str1), len(str2)])
    similary_count = 0
    compare_count = 0
    for i in range(min_len):
        if str1[i] in valid_str:
            compare_count+=1
            if str1[i] == str2[i]:
                similary_count+=1

    return similary_count / compare_count if compare_count != 0 else 0



def hlp(params):
    htp_code = params['htp_code']
    ROOT_DIR = params['ROOT_DIR']
    sequence = params['sequence'].upper()

    block_df = pd.read_csv('{}/dataset/haplotype_database.csv'.format(ROOT_DIR))
    target_df = block_df[block_df['HTP ID'] == htp_code].copy()
    if len(target_df) == 0:
        print('htp code error')
    else:
        target_df['test_sequence'] = sequence
        target_df['similary'] = target_df.apply(lambda x: get_similary(x['test_sequence'], x['Haplotype Sequence']), axis=1)
        target_df['bayes'] = target_df.apply(lambda x: getNBayes(x['Frequency']), axis=1)
        target_df.sort_values(by=['similary', 'bayes'], ascending=[False, False], inplace=True)
        print(target_df.head(1)['Haplotype Sequence'].tolist()[0])


if __name__ == '__main__':
    hlp(params)