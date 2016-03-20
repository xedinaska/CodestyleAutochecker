import subprocess


class SystemCommandRunner:
    isShell = True
    stdout = -1
    stderr = -2

    def __init__(self):
        self.isShell = True
        self.stdout = subprocess.PIPE
        self.stderr = subprocess.STDOUT

    def execute(self, command):
        process = subprocess.Popen(
            command,
            shell=self.isShell,
            stdout=self.stdout,
            stderr=self.stdout,
            universal_newlines=True
        )

        return process.stdout.readlines()
