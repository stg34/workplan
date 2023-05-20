import sys
from srclib.app.purgen import AppPurgen


if __name__ == '__main__':
    plan = AppPurgen(sys.argv[1:])
    ret = plan.purge()
    exit(ret)
