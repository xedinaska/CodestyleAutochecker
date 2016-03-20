import os

from configuration_builder import ConfigurationBuilder
from system_command_runner import SystemCommandRunner
from git_handler import GitHandler

bash_profile_file = '/Users/Xedin/.bash_profile'

phpcs_repo = 'git://github.com/squizlabs/PHP_CodeSniffer.git'

def make_config():
    configuration_builder = ConfigurationBuilder()
    configuration_builder.build()


def get_command_runner():
    command_runner = SystemCommandRunner()
    return command_runner


def get_git_handler():
    git_handler = GitHandler(os.path.dirname(os.path.abspath(__file__)))
    return git_handler


def make_alias():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    command = 'python3 ' + current_dir + '/preprocessor.py'
    alias = '\n\nalias precommit="' + command + ' $1"'

    file = open(bash_profile_file, 'a')
    file.write(alias)
    file.close()

    get_command_runner().execute('source ' + bash_profile_file)


def download_phpcs():
    get_git_handler().clone(phpcs_repo)


def install():
    download_phpcs()
    make_config()
    make_alias()

install()
