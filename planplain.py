import sys
from srclib.app.plain_plan import AppPlanPlain


if __name__ == '__main__':
    plan = AppPlanPlain(sys.argv[1:])
    ret = plan.build()
    exit(ret)
