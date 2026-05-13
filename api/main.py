from fastapi import FastAPI
from datetime import date

from workflows.run_daily_news import run_daily_news

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/run-news")
async def run_news():
    today = str(date.today())
    result = await run_daily_news(today)
    return result
