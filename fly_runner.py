import schedule
import time
from bot import main as run_bot


def job():
    print("Running bot...")
    run_bot()


schedule.every(5).minutes.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
