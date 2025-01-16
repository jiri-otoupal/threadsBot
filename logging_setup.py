import logging

from rich.logging import RichHandler


def setup_logging(level=logging.INFO):
    """Setup the general logging configuration for the entire application."""
    # Create a root logger
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)]
    )
