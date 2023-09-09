from fastapi import FastAPI
import schedule
import time
from fastapi_utils.tasks import repeat_every

from email_parsing import parse_unread_emails

app = FastAPI()


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # repeat every 24h
def initialization():
    print("executing periodic reading of emails")
    """
    schedule.every().day.at("00:00").do(parse_unread_emails)

    # Run the scheduler continuously.
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 10 second to avoid high CPU usage

    """

@app.get("/")
async def root():
    return {"message": "Resume sending API is up and running!"}