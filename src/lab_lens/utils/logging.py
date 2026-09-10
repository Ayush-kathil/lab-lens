import logging
import sys

def setup_logger(name: str = "lab_lens", level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if already setup
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger

logger = setup_logger()
