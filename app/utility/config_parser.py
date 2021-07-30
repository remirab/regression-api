import yaml
import re
import os

# matches environment variables in yaml config
path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')

def path_constructor(loader, node):
    return os.path.expandvars(node.value)


class EnvVarLoader(yaml.SafeLoader):
    pass


class YamlParser(object):
    """
    Loads yaml config files
    """

    @staticmethod
    def parse_config_file(config_path, config_key, load_env_vars=False):
        config_dict = None

        loader = yaml.SafeLoader

        if load_env_vars:
            print("ConfigParser: Load env vars...")
            EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
            EnvVarLoader.add_constructor('!path', path_constructor)
            loader = EnvVarLoader

        with open(config_path) as config_file:
            try:
                config_dict = yaml.load(config_file, Loader=loader)[config_key]
            except yaml.YAMLError as error:
                print(error)

        return config_dict
