import datetime
import os
import sys

from apscheduler.scheduler import Scheduler

from XinJuKe.settings import BASE_DIR


def clear_session():
    os.chdir(BASE_DIR)
    python_env = sys.executable
    cmd = '%s manage.py clearsessions' % python_env
    os.system(cmd)
    log = '[%s]自动清理过期session, cmd:<%s>'% (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), cmd)
    print(log)
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'crontab_clear_session.log')
    with open(log_path, 'a+') as f:
        f.write(log + '\n')


sched = Scheduler()  # 实例化，固定格式


@sched.interval_schedule(seconds=60 * 10)  # 装饰器，seconds=60意思为该函数为1分钟运行一次
def mytask():
    clear_session()


sched.start()  # 启动该脚本


