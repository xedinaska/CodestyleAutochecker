from system_command_runner import SystemCommandRunner


class GitHandler:

    command_runner = None
    project_path = ''

    def __init__(self, project_path):
        self.command_runner = SystemCommandRunner()
        self.project_path = project_path

    def status(self):
        git_status_command = 'cd ' + self.project_path + ' && git status'
        system_response = self.command_runner.execute(command=git_status_command)

        return system_response

    def commit(self, message):
        git_commit_command = 'cd ' + self.project_path + ' && git commit -m "' + message + '"'
        system_response = self.command_runner.execute(command=git_commit_command)

        return system_response

    def clone(self, repo):
        git_clone_command = 'cd ' + self.project_path + ' && git clone ' + repo
        system_response = self.command_runner.execute(command=git_clone_command)

        return system_response
