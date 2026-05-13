from apscheduler.schedulers.asyncio import AsyncIOScheduler
from workflows.run_daily_news import run_daily_news
from datetime import date

scheduler = AsyncIOScheduler()


def start_scheduler():
    scheduler.add_job(
        lambda: run_daily_news(str(date.today())),
        "cron",
        hour=8,
        minute=0,
    )
    scheduler.start()
