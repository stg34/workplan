# encoding: utf-8

from pathlib import Path
from srclib.arguments.base_arguments import BaseArguments


class PlanArguments(BaseArguments):
    @property
    def arg_defs(self):
        args = {
            'out_md': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': 'plan.md'}
                },
                'args': {
                    'names': ['-o', '--out-md'],
                    'other': {
                        'help': 'Document filename. Default is PL plan.md'
                    }
                }
            },
            'scale': {
                'config': {
                    'method': 'getfloat',
                    'params': {'fallback': 1}
                },
                'args': {
                    'names': ['-s', '--scale'],
                    'other': {
                        'type': float,
                        'help': 'Multiplier to estimate hours'
                    }
                }
            },
            'work_hours': {
                'config': {
                    'method': 'getint',
                    'params': {'fallback': None}
                },
                'args': {
                    'names': ['-w', '--work-hours'],
                    'other': {
                        'type': int,
                        'help': 'Number of working hours per day'
                    }
                }
            },
            'h_start_level': {
                'config': {
                    'method': 'getint',
                    'params': {'fallback': 1}
                },
                'args': {
                    'names': ['--h-start-level'],
                    'other': {
                        'type': int,
                        'help': 'Level of the first header in the document. 1: <H1>...</H1>, 2: <H2>...</H2>, ...'
                    }
                }
            }
        }

        return super().arg_defs | args

    @property
    def out_md_path(self):
        return Path(self.out_dir).joinpath(self.out_md)
