import os
import logging
from datetime import datetime

def setup_logging(log_dir='logs', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    """
    This function sets up the logging for all modules. Means we repeat ourselves less. 

    Example:
        Initialise once in ``main.py``::

            logger = setup_logging()

        Then in every other script, retrieve the logger with one of::

            logger = logging.getLogger(__name__)
            logger = logging.getLogger("Main")
            logger = logging.getLogger()

    Args:
        log_dir (str): The filepath where log files will live.
        format (str): Format each log line with a timestamp, name, level, and message

    Returns:
        Logger instance
    """
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f'{log_dir}/{timestamp}.log'

    # Set level

    logging.basicConfig(
        filename=log_filename,
        format=format,    # format as time, level, and message
        level=logging.INFO                                      # lowest level you want to capture with logs
    )
    return logging.getLogger()