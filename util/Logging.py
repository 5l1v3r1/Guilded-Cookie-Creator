import logging

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;203m[\x1b[0m%(asctime)s\x1b[38;5;203m] \x1b[0m| \x1b[38;5;203m%(message)s",
    datefmt="%I:%M:%S",
)