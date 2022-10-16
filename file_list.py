import subprocess
import re

class FileListError(Exception):
    def __init__(self, command, error):
        self.command = command
        self.error = error

class FileList():
    def __init__(self, base_branch):
        self.base_branch = base_branch

    def execute_command(self, command, verbose = True):
        res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF8")

        if res.returncode != 0: raise FileListError(command, res.stderr)
        print(command)
        print(res.stdout)
        return res.stdout.splitlines()

    def list(self):
        file_names = []
        file_names = self.execute_command("git -c core.quotepath=false ls-files --modified")
        file_names += self.execute_command("git -c core.quotepath=false diff --name-only --cached")
        file_names += self.execute_command("git -c core.quotepath=false ls-files --others --exclude-standard")
        file_names += self.execute_command(f"git -c core.quotepath=false diff --name-only ..{self.base_branch}")
        file_names = list(set(file_names))
        file_names.sort()
        
#        file_names = list(filter(lambda f: f.endswith('txt'), file_names)) # TODO: fixme
        return file_names
