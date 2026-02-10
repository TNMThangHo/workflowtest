import logging
import sys
from pathlib import Path

def setup_logger(name: str = "TestGen", log_file: str = "test_gen.log", level=logging.INFO):
    """
    Setup a standardized logger that outputs to both console and file.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Formatters
    console_formatter = logging.Formatter('%(message)s')  # Simple format for console
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File Handler
    try:
        log_path = Path("logs")
        log_path.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_path / log_file, encoding='utf-8')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not set up file logging: {e}")

    return logger

# Singleton instance
log = setup_logger()
