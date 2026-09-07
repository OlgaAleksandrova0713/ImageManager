import logging
import os

from config import LOGS_DIR

os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)

