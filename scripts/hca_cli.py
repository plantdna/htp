import click
import os
import traceback
from multiprocessing import cpu_count

from scripts.hca.index import hca

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ROOT_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', 'input_path', help="input file path.", prompt='Please type input file path', type=click.Path(exists=True))
@click.option('-c', '--contrast', 'contrast_path', help="contrast file path.", prompt='Please type contrast file path', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_dir', help="output dir path.", prompt='Please type output dir path', type=click.Path(exists=True), default='{}/output'.format(ROOT_DIR), show_default=True)
@click.option('-ms', '--missing_string', 'ms', help="missing string.", prompt='Please type missing string', default='---', show_default=True, type=click.STRING)
@click.option('-p', '--process', 'process', help="cup core number.", prompt='Please type number of process', default=1, show_default=True, type=click.IntRange(1, cpu_count(), clamp=True))

def cli(input_path, contrast_path, output_dir, ms, process):
    try:
        hca({
            'compare_file_path': input_path,
            'contrast_file_path': contrast_path,
            'ms': ms,
            'output_path': output_dir,
            'process': process,
        })
    except Exception as e:
        traceback.print_exc()