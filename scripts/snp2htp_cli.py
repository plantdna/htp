import click
import os
import traceback
import time


from scripts.snp2htp.split_genotyping_file import split_genotyping_file_by_chr
from scripts.snp2htp.generator_htp_sequence import generator_htp_sequence
from scripts.snp2htp.generator_htp_index import generator_htp_index

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ROOT_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', 'input_path', help="input file path.", prompt='Please type input file path', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_dir', help="output dir path.", prompt='Please type output dir path', type=click.Path(exists=True), default='{}/output'.format(ROOT_DIR), show_default=True)

def cli(input_path, output_dir):
    try:
        timestamp = int(round(time.time() * 1000))
        genotyping_file_name = input_path.split('/')[-1].split('.')[0]
        output_path = '{}/{}_{}'.format(output_dir, genotyping_file_name, timestamp)

        split_genotyping_file_by_chr({
            'file_path': input_path,
            'output_path': '{}/step1'.format(output_path),
        })
        generator_htp_sequence({
            'data_path': '{}/step1'.format(output_path),
            'output_path': '{}/step2'.format(output_path),
            'ROOT_DIR': ROOT_DIR,
        })
        generator_htp_index({
            'data_path': '{}/step2'.format(output_path),
            'output_path': '{}/step3'.format(output_path),
            'htp_file_path': output_path,
            'ROOT_DIR': ROOT_DIR,
        })
    except Exception as e:
        traceback.print_exc
