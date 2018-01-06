from apscheduler.schedulers.blocking import BlockingScheduler
from veg_recipe_bot import tweet

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=13, timezone='UTC')
def scheduled_job():
    tweet()


sched.start()