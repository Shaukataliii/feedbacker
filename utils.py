import yaml

def load_yaml_config(path: str):
    with open(path, 'r') as file:
        return yaml.safe_load(file)