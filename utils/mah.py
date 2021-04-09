from graia.application import Session
import yaml


def mah_config(config_path: str) -> Session:
    f = open(config_path,encoding='utf-8').read()
    c = yaml.load(f, Loader=yaml.SafeLoader)
    return Session(**c)
