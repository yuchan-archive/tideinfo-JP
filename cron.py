#! /usr/bin/env python

from apscheduler.scheduler import Scheduler
import tweet

sched = Scheduler()

def timed_job():
    tweet.updateTideInfo()

sched.start()
sched.add_cron_job(timed_job, hour='15-21', minute='*')

while True:
    pass
