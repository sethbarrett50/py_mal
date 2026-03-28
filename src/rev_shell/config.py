from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ShellConfig(BaseSettings):
    host: str = Field(default='127.0.0.1', description='Listener IP or Hostname')
    port: int = Field(default=4444, ge=1, le=65535)
    buffer_size: int = Field(default=4096, ge=1024)
    log_file: str = Field(default='rev_shell.log')

    model_config = SettingsConfigDict(env_prefix='VPS_')
