# encoding: utf-8

import subprocess
import pathlib
import gettext


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


def wrap_error(text):
    return Color.FAIL + text + Color.ENDC


def wrap_warning(text):
    return Color.WARNING + text + Color.ENDC


def wrap_success(text):
    return Color.OKGREEN + text + Color.ENDC


def print_error(text):
    print(wrap_error('=' * 80) + "\n")
    print(wrap_error(text))
    print("\n" + wrap_error('=' * 80))


def print_warning(text):
    print(wrap_warning('=' * 80) + "\n")
    print(wrap_warning(text))
    print("\n" + wrap_warning('=' * 80))


def print_success(text):
    print(wrap_success('=' * 80) + "\n")
    print(wrap_success(text))
    print("\n" + wrap_success('=' * 80))


class ExecuteCommandError(Exception):
    def __init__(self, command, stdout, stderr, ret):
        self.command = command
        self.stderr = stderr
        self.stdout = stdout
        self.ret = ret


def execute_command(command, verbose=False, skip_error=False):
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF8")

    if verbose:
        print('Command:')
        print(command)
        print('Retcode:')
        print(res.returncode)
        print('Stdout:')
        print(res.stdout)
        print('Stderr:')
        print(res.stderr)

    if not skip_error and res.returncode != 0:
        raise ExecuteCommandError(command, res.stdout, res.stderr, res.returncode)

    return res.stdout.splitlines()


def branch_name():
    return ''.join(execute_command('git rev-parse --abbrev-ref HEAD'))


def format_num(time):
    if time is None:
        return ''

    return f'{time:.1f}'.rstrip('0').rstrip('.')


def hex_to_rgb(hex):
    return [int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]


def rgb_to_hex(rgb):
    return f'#{rgb[0]:x}{rgb[1]:x}{rgb[2]:x}'


def setup_i18n(localedir, domain):
    localedir = f'{pathlib.Path(__file__).parent.resolve()}/{localedir}/locales'

    t = gettext.translation(domain, localedir, fallback=True)
    return t.gettext
