import os
from .base import split_genotype_file, merge_chrs


def groupby_chr(genotyping_files_dir:str, board_dir:str, skiprows:int, chr_dir:str) -> None:
    '''
    按染色体拆分下机数据文件, 并合并到数据集
    '''
    genotyping_files = [filename for filename in os.listdir(genotyping_files_dir) if filename[0] != '.']
    for filename in genotyping_files:
        genotyping_file_path = '{}/{}'.format(genotyping_files_dir, filename)

        split_dir = '{}/{}'.format(board_dir, filename.split('.')[0])
        if os.path.exists(split_dir):
            os.system('rm -rf {}'.format(split_dir))

        split_genotype_file(
            genotyping_file_path,
            '{}/{}'.format(board_dir, filename.split('.')[0]),
            skiprows
        )

        merge_chrs('{}/{}'.format(board_dir, filename.split('.')[0]), chr_dir)

