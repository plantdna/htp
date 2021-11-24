import click
import os
import traceback

from scripts.hpb.index import hpb

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ROOT_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', 'input_path', help="group htp data files dir.", prompt='Please type input genotype files dir', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_path', help="output path.", prompt='Please type output dir path', type=click.Path(exists=False))

def cli(input_path, output_path):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        hpb({
            'input_path': input_path,
            'output_path': output_path,
            'ROOT_DIR': ROOT_DIR,
        })
    except Exception as e:
        traceback.print_exc()