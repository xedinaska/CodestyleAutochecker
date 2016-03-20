import json


class ConfigurationBuilder:
    config_file = 'config.json'

    default_configuration = {
        'codesniffer_path': 'php_codesniffer/scripts/phpcs',
        'project_path': '~/Sites/s7project/Whitelabel/ClientBundle/Controller',
        'severity_level': 'WARNING',
        'ignore_view_files': 'true',
        'view_files_extensions': '.html,.html.twig',
        'ignore_js': 'true',
        'js_files_extensions': '.js,.jsx'
    }

    config = {}

    def __init__(self, config_file=None):
        if config_file is not None:
            self.config_file = config_file

    def ask_for_keys(self):
        for key in self.default_configuration:
            value = input('Please put "' + key + '" config value (default: ' + self.default_configuration[key] + '): ')

            if not value:
                self.check_for_array_value(key, self.default_configuration[key])
            else:
                self.check_for_array_value(key, value)

    def check_for_array_value(self, key, value):
        if ',' not in value:
            self.config[key] = value
        else:
            self.config[key] = value.split(',')

    def get_config_string(self):
        json_result = json.dumps(self.config)
        return json_result

    def save_config(self):
        file = open(self.config_file, 'w')
        file.write(self.get_config_string())
        file.close()

    def build(self):
        self.ask_for_keys()
        self.save_config()
