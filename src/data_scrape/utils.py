import re


def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def extract_passwords_regex(data):
    return re.findall(r'password":"([^"]*)', data)
