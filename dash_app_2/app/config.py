from pydantic import BaseModel
from pathlib import Path
import tomllib
import os


CONFIG_PATH = os.getenv("CONFIG_PATH", Path(__file__).parent.parent.resolve() / "config/config.toml")


class Config(BaseModel):
    connection_string: str
    api_token: str
    api_url: str


def load_config() -> Config:
    config_raw = tomllib.loads(
        Path(CONFIG_PATH).read_text()
    )
    config = Config(**config_raw)

    return config