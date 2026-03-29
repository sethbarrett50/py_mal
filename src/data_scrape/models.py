from pydantic import BaseModel


class BrowserList(BaseModel):
    browsers: list[str]


class ScrapeArgs(BaseModel):
    browser_list: BrowserList
    output_file_passwords: str
    output_file_crypto_keys: str
