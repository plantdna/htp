import click
import traceback
import datetime
import time
import os

from scripts.snp2htp.split_genotyping_file import split_genotyping_file_by_chr
from scripts.snp2htp.generator_htp_sequence import generator_htp_sequence
from scripts.snp2htp.generator_htp_index import generator_htp_index

from scripts.wghca.index import wghca
from scripts.hca.index import hca

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ROOT_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    '-m', '--mode', 'mode', 
    help="mode options.", 
    prompt='Please select mode', 
    type=click.Choice(['snp2htp', 'wghca', 'hca'], case_sensitive=False),
)

@click.option('-i', '--input', 'input_path', help="input file path.", prompt='Please type input file path', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_dir', help="output dir path.", prompt='Please type output dir path', type=click.Path(exists=True), default='{}/output'.format(ROOT_DIR), show_default=True)
@click.option('-c', '--contrast', 'contrast_path', help="contrast file path (This is required when the mode is HCA and WGHCA).", prompt='Please type contrast file path', default='/', show_default=True, type=click.Path(exists=True))
@click.option('-st', '--similarity_threshold', 'st', help="similarity threshold.", prompt='Please type similarity threshold', default=0.8, show_default=True, type=click.FLOAT)
@click.option('-ms', '--missing_string', 'ms', help="missing string.", prompt='Please type missing string', default='---', show_default=True, type=click.STRING)

def cli(mode, input_path, output_dir, contrast_path, st, ms):
    """
    Welcome use htp cli
    """
    try:
        start_time = datetime.datetime.now()
        timestamp = int(round(time.time() * 1000))
        if mode == 'snp2htp':
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

            click.echo('The result file has been generated: {}/all_htps.csv'.format(output_path))

        elif mode == 'wghca':
            wghca({
                'compare_file_path': input_path,
                'contrast_file_path': contrast_path,
                'ms': ms,
                'st': st,
                'output_path': output_dir
            })

            click.echo('The result file has been generated: {}/wghca_compare_result.csv'.format(output_dir))

        elif mode == 'hca':
            hca({
                'compare_file_path': input_path,
                'contrast_file_path': contrast_path,
                'ms': ms,
                'output_path': output_dir
            })
            click.echo('The result file has been generated: {}/hca_compare_result.csv'.format(output_dir))
        else:
            click.echo('mode error')

        click.echo(datetime.datetime.now()-start_time)

    except Exception as e:
        traceback.print_exc()
