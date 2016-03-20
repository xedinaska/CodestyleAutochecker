class ConfigurationLoader:

    configuration = {}

    def __init__(self, json_config_data):
        self.configuration = json_config_data

    def get_project_path_value(self):
        return self.configuration.get('project_path')

    def get_codesniffer_path_value(self):
        return self.configuration.get('codesniffer_path')

    def get_severity_level_value(self):
        return self.configuration.get('severity_level')

    def get_ignore_view_files_value(self):
        return self.configuration.get('ignore_view_files')

    def get_view_files_extensions_list(self):
        return self.configuration.get('view_files_extensions')

    def get_ignore_js_files_value(self):
        return self.configuration.get('ignore_js')

    def get_js_files_extensions_list(self):
        return self.configuration.get('js_files_extensions')