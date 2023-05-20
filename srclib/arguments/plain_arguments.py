# encoding: utf-8

# from srclib.utils import branch_name
from srclib.arguments.plan_arguments import PlanArguments


class PlainArguments(PlanArguments):
    @property
    def arg_defs(self):
        args = {
            # TODO: title
        }

        return super().arg_defs | args
