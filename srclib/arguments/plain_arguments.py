# encoding: utf-8

from srclib.arguments.plan_arguments import PlanArguments


class PlainArguments(PlanArguments):
    @property
    def arg_defs(self):
        args = {
            'title': {
                'config': {
                    'method': 'get',
                    'params': {'fallback': None}
                },
                'args': {
                    'names': ['-t', '--title'],
                    'other': {
                        'help': 'Document title. Default is branch name'
                    }
                }
            }
        }

        return super().arg_defs | args
