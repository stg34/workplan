# encoding: utf-8

from pathlib import Path
from srclib.view.dot.color_scheme import ViewDotColorScheme
from srclib.arguments.plan_arguments import PlanArguments


class GraphArguments(PlanArguments):
    @property
    def arg_defs(self):
        args = {
            'out_graph': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': 'plan.png'}
                },
                'args': {
                    'names': ['-p', '--out-graph'],
                    'other': {
                        'help': 'Diagramm filename. Default is PL plan.png'
                    }
                }
            },
            'dot_binary_path': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': 'dot'}
                },
                'args': {
                    'names': ['--dot-binary-path'],
                    'other': {
                        'help': 'dot binary path. Default is dot'
                    }
                }
            },
            'reverse': {
                'config': {
                    'method': 'getboolean',
                    'params': {'fallback': False}
                },
                'args': {
                    'names': ['-r', '--reverse'],
                    'other': {
                        'action': 'store_true',
                        'help': 'Reverse the arrows on the diagram'
                    }
                }
            },
            'graph_dir': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': 'tb'}
                },
                'args': {
                    'names': ['--graph-dir'],
                    'other': {
                        'default': 'tb',
                        'choices': ['tb', 'lr'],
                        'help': 'Graph direction: top-to-bottom or left-to-right'
                    }
                }
            },
            'color_scheme': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': 'COLOR_SCHEME_DARK'}}
            }
        }

        return super().arg_defs | args

    @property
    def out_graph_path(self):
        return Path(self.out_dir).joinpath(self.out_graph)

    @property
    def dot_color_scheme(self):
        return ViewDotColorScheme(self.config, self.color_scheme)
