import click
import os
import traceback

from scripts.hlp.index import hlp

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ROOT_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-s', '--sequence', 'sequence', help="sequence.", prompt='Please type input your sequence', type=click.STRING)
@click.option('-c', '--code', 'htp_code', help="htp code.", prompt='Please type HTP code', type=click.STRING)

def cli(input_path, output_path):
    try:
        hlp({
            'htp_code': input_path,
            'sequence': output_path
        })
    except Exception as e:
        traceback.print_exc()