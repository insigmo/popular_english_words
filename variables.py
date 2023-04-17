import os
from pathlib import Path

from environs import Env


def _set_local_settings() -> None:
    hosts = ["POSTGRES_HOST", "RABBITMQ_HOST", "SELENOID_HOST"]
    for host in hosts:
        os.environ[host] = '127.0.0.1'


CONFIG_PATH = Path(__file__).parent / 'build/dev.env'
if CONFIG_PATH.exists():
    env = Env()
    env.read_env(str(CONFIG_PATH))

if os.getenv('LOCAL') == 'True':
    _set_local_settings()


class Vars:
    api_token = os.getenv("TELEGRAM_API_TOKEN")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_port = int(os.getenv("POSTGRES_PORT"))


if __name__ == '__main__':
    v = Vars()
    print(v.postgres_user)
