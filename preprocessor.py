import json
import sys
import os

from git_handler import GitHandler
from system_command_runner import SystemCommandRunner
from configuration_loader import ConfigurationLoader
from severity import Severity


class Preprocessor:
    config_file = 'config.json'
    configuration = {}

    command_runner = None
    git_handler = None

    def __init__(self):
        self.config_file = os.path.dirname(os.path.abspath(__file__)) + '/config.json'
        config_data = self.load_configuration()

        self.command_runner = SystemCommandRunner()
        self.configuration = ConfigurationLoader(json_config_data=config_data)
        self.git_handler = GitHandler(project_path=self.configuration.get_project_path_value())

    def execute(self):
        errors = self.validate()

        if errors.__len__() > 0:
            self.show_errors(errors)
        else:
            self.do_commit()

    def validate(self):
        files_to_check = self.get_files_to_check_list()

        if files_to_check.__len__() <= 0:
            return []

        errors = {}
        filename = ''
        appendable = True

        files_to_check = " ".join(files_to_check)

        phpcs_run_command = self.configuration.get_codesniffer_path_value() + ' --standard=PSR2' + files_to_check
        phpcs_response = self.command_runner.execute(command=phpcs_run_command)

        break_point_list = self.get_break_points()

        for line in phpcs_response:
            if 'FILE:' in line:
                filename = line.split(':')[1].strip()

            if any(break_point in line for break_point in break_point_list):
                data = line.split('|')

                if data.__len__() == 3:

                    if not errors.get(filename):
                        errors[filename] = []

                    errors[filename].append({
                        'line': data[0].strip(),
                        'message': data[2].strip()
                    })
                appendable = True
            elif line.split('|').__len__() > 1 and line.split('|')[0].isspace() and appendable:
                errors[filename][-1]['message'] += ' ' + line.split('|')[2].strip()
            else:
                appendable = False

        return errors

    def load_configuration(self):
        with open(self.config_file) as config_data_file:
            config_data = json.load(config_data_file)

        return config_data

    def get_files_to_check_list(self):
        files_to_check = []
        add_to_check_list = False

        files_to_commit = self.git_handler.status()

        for line in files_to_commit:

            if 'Changes to be committed' in line:
                add_to_check_list = True
            elif 'Untracked files' in line or 'Changes not staged for commit' in line:
                add_to_check_list = False
            elif '.php~' in line:
                add_to_check_list = False

            if add_to_check_list is True and ('new file' in line or 'modified' in line):
                filename = self.configuration.get_project_path_value() + '/' + line.split(':')[1].strip()

                if self.configuration.get_ignore_view_files_value():
                    if any(view_files_extension in filename
                           for view_files_extension in
                           self.configuration.get_view_files_extensions_list()):
                        continue

                if self.configuration.get_ignore_js_files_value():
                    if any(js_files_extension in filename
                           for js_files_extension in
                           self.configuration.get_js_files_extensions_list()):
                        continue

                files_to_check.append(filename)

        return files_to_check

    @staticmethod
    def show_errors(self, errors):
        for file in errors:
            print('')
            print(file)
            error_list = errors.get(file)
            for error in error_list:
                print('- ' + error.get('message') + '(line: ' + error.get('line') + ')')

    def get_break_points(self):
        severity_level = self.configuration.get_severity_level_value()

        break_points = [Severity.ERROR]

        if severity_level == Severity.WARNING:
            break_points.append(Severity.WARNING)

        return break_points

    def do_commit(self):
        commit_message = sys.argv[1]
        commit_response = self.git_handler.commit(message=commit_message)

        for line in commit_response:
            print(line)


preprocessor = Preprocessor()
preprocessor.execute()
