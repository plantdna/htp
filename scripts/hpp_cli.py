import click
import os
import traceback

from scripts.hpp.index import hpp

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ROOT_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', 'input_path', help="hybrid file path.", prompt='Please type hybrid file path', type=click.Path(exists=True))
@click.option('-g', '--group_dataset_dir', 'group_dataset_dir', help="group dataset dir.", prompt='Please type group dataset dir', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_path', help="output path.", prompt='Please type output path', type=click.Path(exists=False))

def cli(input_path, group_dataset_dir, output_path):
    try:
        hpp({
            'input_path': input_path,
            'group_dataset_dir': group_dataset_dir,
            'output_path': output_path
        })
    except Exception as e:
        traceback.print_exc()