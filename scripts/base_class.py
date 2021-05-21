import os
import traceback    # traceback.format_exc() return error string
import os

class BaseClass:
    def __init__(self):
        # 初始化 类属性
        pass
    
    def append_write_csv_by_df(self, df, dir_path:str, file_name:str):
        '''
        以追加的方式将DataFrame写成CSV文件
        '''
        try:
            file_path='{}/{}.csv'.format(dir_path, file_name)
            if os.path.exists(dir_path):
                if os.path.exists(file_path):
                    df.to_csv(file_path, mode='a',index=False, header=False, encoding='utf-8_sig')
                else:
                    df.to_csv(file_path, index=False, encoding='utf-8_sig')            
            else:
                os.makedirs(dir_path)
                df.to_csv(file_path, index=False, encoding='utf-8_sig')

            return
        except Exception as e:
            traceback.print_exc()

    def append_write_csv_by_list(self, row:list, dir_path:str, file_name:str):
        '''
        以追加的方式将行数据(list)写成CSV文件
        '''
        try:
            file_path='{}/{}.csv'.format(dir_path, file_name)
            if os.path.exists(dir_path):
                if os.path.exists(file_path):
                    with open(file_path, 'a+',encoding='utf-8') as f:
                        f.write('{}\n'.format(','.join([str(val) for val in row])))
                        f.close()
                else:
                    with open(file_path, 'w',encoding='utf-8') as f:
                        f.write('{}\n'.format(','.join([str(val) for val in row])))
                        f.close()           
            else:
                os.makedirs(dir_path)
                with open(file_path, 'w',encoding='utf-8') as f:
                    f.write('{}\n'.format(','.join([str(val) for val in row])))
                    f.close()
            return
        except Exception as e:
            traceback.print_exc()


    def handle_format(self, val):
        '''
        格式化规则
        '''
        if val == '-':
            return 'D'
        else:
            return 'I'

    def format_indel_allele(self, allele):
        '''
        格式化indel标记基因型
        '''
        try:
            if allele == '---':
                return '---'
            else:
                geno = allele.split('/')
                return '/'.join([self.handle_format(val) for val in geno])

        except Exception as e:
            traceback.print_exc()


    def similar_rate(self, str1:str, str2:str):
        '''
        计算两条基因序列的相似度
        '''
        try:
            min_len_str = str1
            max_len_str = str2
            if len(str1) > len(str2):
                min_len_str = str2
                max_len_str = str1

            common_num = 0
            missing_num = 0
            for i in range(len(min_len_str)):
                if min_len_str[i] == max_len_str[i]:
                    common_num+=1
                if min_len_str[i] == '-':
                    missing_num += 1

            if (len(min_len_str)-missing_num) == 0:
                return 0
            else:
                return round(common_num/(len(min_len_str)-missing_num), 3)

        except Exception as e:
            traceback.print_exc()