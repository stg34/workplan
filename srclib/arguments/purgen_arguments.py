# encoding: utf-8

from pathlib import Path
from srclib.arguments.base_arguments import BaseArguments


class PurgenArguments(BaseArguments):
    @property
    def arg_defs(self):
        args = {
            'out_patch': {
                'config': {'method': 'get', 'params': {'fallback': 'plan.patch'}},
                'args': {'names': ['-o', '--out-patch'], 'other': {}}
            },
            'dry_run': {
                'config': {'method': 'getboolean', 'params': {'fallback': False}},
                'args': {'names': ['--dry-run'], 'other': {'action': 'store_true'}}
            },
        }

        return super().arg_defs | args

    @property
    def out_patch_path(self):
        return Path(self.out_dir).joinpath(self.out_patch)
