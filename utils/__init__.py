import logging
import re


def get_logger(name, filename=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # LOGGER FILE HANDLER
    # if not os.path.exists("Logs"):
    #     os.mkdir("Logs")
    # fh = logging.FileHandler(f"Logs/{filename if filename else name}.log")
    # fh.setLevel(logging.DEBUG)
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    # LOGGER STREAM HANDLER
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def parse_course_id(url: str) -> str:
    result = re.search(r"\/courses\/(\d+)\/?", url)
    if result:
        return result.group(1)
    return ''


def parse_discussion_id(url: str) -> str:
    result = re.search(r"\/discussion_topics\/(\d+)\/?", url)
    if result:
        return result.group(1)
    return ''


def parse_assignment_id(url: str) -> str:
    result = re.search(r"\/assignments\/(\d+)\/?", url)
    if result:
        return result.group(1)
    return ''
