import os
import sys
from loguru import logger
from app.config.settings import ENV

# Determine log level based on environment config
log_level = "DEBUG" if ENV == "development" else "INFO"

# Ensure logs directory exists in the workspace root
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "app.log")

# Configure loguru: remove default handler, add custom stdout and file handlers
logger.remove()

# Add standard output stream handler
logger.add(
    sys.stdout,
    level=log_level,
    format="[{time:YYYY-MM-DD HH:mm:ss}] {level} in {module}: {message}",
    colorize=True,
)

# Add file handler for persistent logging with rotation
logger.add(
    log_file_path,
    level=log_level,
    format="[{time:YYYY-MM-DD HH:mm:ss}] {level} in {module}: {message}",
    encoding="utf-8",
    rotation="10 MB",
)

