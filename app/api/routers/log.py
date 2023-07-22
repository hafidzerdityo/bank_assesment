import structlog
import logging
from datetime import date

structlog.configure(
    processors=[
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log_file = f"log/app_{date.today()}.log"

# Create a file handler to log messages to the file
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Create a console handler to log messages to the console (stdout)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Get the root logger
root_logger = logging.getLogger()

# Add both file and console handlers to the root logger
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Create the structlog logger
logger = structlog.get_logger()

# Log messages using the structlog logger
logger.info("Informational message")
logger.error("Error message")
