"""
Logging configuration using Loguru.
"""
import sys
from loguru import logger


def setup_logging():
    """Configure structured logging for the application."""
    logger.remove()

    # Console handler — human-readable in dev, JSON in prod
    logger.add(
        sys.stdout,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        level="DEBUG",
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # File handler — always JSON
    logger.add(
        "logs/omniviral_{time:YYYY-MM-DD}.log",
        format="{time} | {level} | {name}:{function}:{line} | {message}",
        level="INFO",
        rotation="00:00",   # New file every midnight
        retention="30 days",
        compression="gz",
        serialize=True,     # JSON format
    )

    # Error file
    logger.add(
        "logs/errors_{time:YYYY-MM-DD}.log",
        format="{time} | {level} | {name}:{function}:{line} | {message}",
        level="ERROR",
        rotation="00:00",
        retention="90 days",
        compression="gz",
        serialize=True,
    )

    return logger
