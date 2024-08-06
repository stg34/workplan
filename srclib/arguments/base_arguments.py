# encoding: utf-8

import configparser
from argparse import ArgumentParser


class BaseArguments():
    def __init__(self, sys_args, config_name='.plangraph.conf'):
        self.sys_args = sys_args
        self.config_name = config_name
        self.config = configparser.ConfigParser()
        self.config.read(config_name)
        self.parser = ArgumentParser()
        self.parse()

    @property
    def arg_defs(self):
        return {
            'base_branch': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': 'master'}
                },
                'args': {
                    'names': ['-b', '--base-branch'],
                    'other': {
                        'help': 'The base git branch (usually master or main) against which the modified files are looked for. By default master'
                    }
                }
            },
            'todo_suffix': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': 'PL'}
                },
                'args': {
                    'names': ['-f', '--todo-suffix'],
                    'other': {
                        'help': 'Suffix in the TODO comment: # TODO: SUFFIX: Default is PL'
                    }
                }
            },
            'out_dir': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': './'}
                },
                'args': {
                    'names': ['-d', '--out-dir'],
                    'other': {
                        'help': 'Directory where files will be written. Default is current dir'
                    }
                }
            },
            'verbose': {
                'config': {
                    'method': 'getboolean',
                    'params': {'fallback': False}
                },
                'args': {
                    'names': ['-v', '--verbose'],
                    'other': {
                        'action': 'store_true',
                        'help': 'Verbose output. Useful for troubleshooting'
                    }
                }
            },
            'git_binary_path': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': 'git'}
                },
                'args': {
                    'names': ['--git-binary-path'],
                    'other': {
                        'help': 'git binary path. Default is git'
                    }
                }
            },
            'exclude_extensions': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': ''}
                },
                'args': {
                    'names': ['--exclude-extensions'],
                    'other': {
                        'help': 'Exclude files with the specified extension from the search. For example: --exclude-extensions=png,sql'
                    }
                }
            },
            'src': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': None}
                },
                'args': {
                    'names': ['--src'],
                    'other': {
                        'help': 'TODO'
                    }
                }
            },
        }

    def parse(self):
        config = self.config

        for key in self.arg_defs:
            method = getattr(config, self.arg_defs[key]['config']['method'])
            value = method('MAIN', key, **self.arg_defs[key]['config']['params'])
            setattr(self, key, value)

            if 'args' in self.arg_defs[key]:
                self.parser.add_argument(*self.arg_defs[key]['args']['names'], **self.arg_defs[key]['args']['other'])

        self.args = self.parser.parse_args(self.sys_args)

        for key in self.arg_defs:
            if 'args' in self.arg_defs[key] and getattr(self.args, key):
                setattr(self, key, getattr(self.args, key))

    @property
    def excluded_extensions(self):
        if self.exclude_extensions:
            return ['.' + e for e in self.exclude_extensions.split(',')]

        return []

    def print(self):
        for key in self.arg_defs:
            print(f'self.{key} = {getattr(self, key)}')
