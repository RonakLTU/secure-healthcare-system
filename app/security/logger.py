import logging
import os

LOG_FILE = "logs/app.log"

# create logs folder if not exist
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_event(message):
    logging.info(message)

def log_error(message):
    logging.error(message)