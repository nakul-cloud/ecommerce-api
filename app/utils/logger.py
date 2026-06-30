import logging
import os
import sys
from app.config.settings import ENV

# Determine log level based on environment config
log_level = logging.DEBUG if ENV == "development" else logging.INFO

# Get named logger
logger = logging.getLogger("ecommerce_api")
logger.setLevel(log_level)

# Create standard formatter
formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Stream handler for standard output
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(log_level)
console_handler.setFormatter(formatter)

# Ensure logs directory exists in the workspace root
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "app.log")

# File handler for persistent logging
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setLevel(log_level)
file_handler.setFormatter(formatter)

# Prevent duplicate handlers
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
