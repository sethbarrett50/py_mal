def test_logger_creation(tmp_path):
    from rev_shell.logger import setup_logger

    log_file = tmp_path / 'test.log'
    logger = setup_logger(str(log_file))
    logger.info('Test message')

    assert log_file.exists()
    assert 'Test message' in log_file.read_text()
