# encoding: utf-8

import sys
from srclib.app.graph_plan import AppPlanGraph


if __name__ == '__main__':
    plan = AppPlanGraph(sys.argv[1:])
    ret = plan.build()
    exit(ret)
