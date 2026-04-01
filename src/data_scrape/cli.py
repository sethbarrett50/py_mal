import click

from .data_scrape import data_scrape
from .models import BrowserList


@click.command()
@click.argument('browser_list', type=BrowserList)
@click.option('--output-file-passwords', default='passwords.txt', type=str)
@click.option('--output-file-crypto-keys', default='crypto_keys.txt', type=str)
def scrape(browser_list, output_file_passwords, output_file_crypto_keys):
    data_scrape(browser_list.browsers, output_file_passwords, output_file_crypto_keys)


if __name__ == '__main__':
    scrape()
