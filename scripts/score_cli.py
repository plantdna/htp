import click
import os
import traceback

from scripts.score.index import score

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ROOT_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', 'groups_path', help="group group data files dir.", prompt='Please type input group files dir', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_path', help="output file path.", prompt='Please type output file path', type=click.Path(exists=False))

def cli(groups_path, output_path):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        score({
            'groups_path': groups_path,
            'output_path': output_path
        })
    except Exception as e:
        traceback.print_exc()