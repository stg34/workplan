import subprocess
import re

class FileListError(Exception):
    def __init__(self, command, error):
        self.command = command
        self.error = error

class FileList():
    def __init__(self):
        pass

    def execute_command(self, command, verbose = False):
        res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF8")

        if res.returncode != 0: raise FileListError(command, res.stderr)

        if verbose:
            print(command)
            for line in res.stdout.splitlines():
                print('    ' + line)

        return res.stdout.splitlines()

    def list(self, base_branch, verbose = False):
        file_names = []
        file_names = self.execute_command("git -c core.quotepath=false ls-files --modified", verbose)
        file_names += self.execute_command("git -c core.quotepath=false diff --name-only --cached", verbose)
        file_names += self.execute_command("git -c core.quotepath=false ls-files --others --exclude-standard", verbose)
        file_names += self.execute_command(f"git -c core.quotepath=false diff --name-only --diff-filter=d {base_branch}..", verbose)
        file_names = list(set(file_names))
        file_names.sort()
        # file_names = filter(lambda f: f != '.planplain.conf', file_names)

        return file_names

    def branch_name(self):
        return ''.join(self.execute_command('git rev-parse --abbrev-ref HEAD'))
