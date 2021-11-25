import click
import os
import traceback

from scripts.abss.index import abss

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ROOT_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-t', '--genotype', 'genotype_files_dir', help="genotype files dir.", prompt='Please type input genotype files dir', type=click.Path(exists=True))
@click.option('-s', '--sample', 'sample_file_path', help="sample file path.", prompt='Please type input sample file path', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_path', help="output file path.", prompt='Please type output file path', type=click.Path(exists=False))

def cli(genotype_files_dir, sample_file_path, output_path):
    try:
        abss({
            'genotype_files_dir': genotype_files_dir, 
            'sample_file_path': sample_file_path, 
            'output_path': output_path,
            'ROOT_DIR': ROOT_DIR,
        })
    except Exception as e:
        traceback.print_exc()