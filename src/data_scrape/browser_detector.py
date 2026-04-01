def detect_browser_type(process_name):
    if process_name in ['chrome.exe', 'firefox.exe']:
        return process_name.split('.')[0]
    elif process_name.startswith('safari'):
        return 'Safari'
    else:
        return None
