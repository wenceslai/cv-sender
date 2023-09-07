from fastapi import FastAPI
import schedule
import time

from email_parsing import parse_unread_emails

app = FastAPI()


@app.on_event("startup")
def initialization():
    schedule.every().day.at("00:00").do(parse_unread_emails)

    # Run the scheduler continuously.
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 10 second to avoid high CPU usage


@app.get("/")
async def root():
    return {"message": "Resume sending API is up and running!"}