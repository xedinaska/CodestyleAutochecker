import os

from configuration_builder import ConfigurationBuilder
from system_command_runner import SystemCommandRunner

bash_profile_file = '/Users/Xedin/.bash_profile'


def make_config():
    configuration_builder = ConfigurationBuilder()
    configuration_builder.build()


def get_command_runner():
    command_runner = SystemCommandRunner()
    return command_runner


def make_alias():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    command = 'python3 ' + current_dir + '/preprocessor.py'
    alias = '\n\nalias precommit="' + command + ' $1"'

    file = open(bash_profile_file, 'a')
    file.write(alias)
    file.close()

    get_command_runner().execute('source ' + bash_profile_file)


def install():
    make_config()
    make_alias()

install()
