import json
import traceback


class Configuration:
    config: dict = None

    @staticmethod
    def setup(path):
        """
        Set the configuration to the given config file

        :param str path: path to the desired configuration file
        """
        with open(path, 'r') as f:
            Configuration.config = json.load(f)

    @staticmethod
    def path() -> str:
        """
        Path to which dataset to use

        :return: Path to a folder containing exercise data
        :rtype: str
        """
        if Configuration.config['debug']:
            return "data/cleaned-regrouped-small"
        return "data/cleaned-regrouped"

    @staticmethod
    def get(key):
        """
        Retrieve the requested key from the config file

        :param str key: String of the key to retrieve from the config file
        :returns: Value of the requested key
        :rtype: mixed
        """
        try:
            Configuration.config[key]
        except KeyError:
            print('-----WARNING-----')
            print(traceback.format_exc().splitlines()[-1])  # Only print the invalid key
            print('Requested invalid key... Consider adding it to the config file if this is intended')
            print('Returning False')
            print('-----------------')
            return False
        else:
            return Configuration.config[key]
