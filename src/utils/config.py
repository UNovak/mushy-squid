import yaml


def load(path: str = "./config/config.yml") -> dict:
    with open(path) as file:
        return yaml.safe_load(file)
