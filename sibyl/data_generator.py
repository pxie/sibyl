import random
from logger import log


def rand(total_number):
    log.info("generate random data from 0 - 1")
    if total_number < 0:
        return log.info("input total_number is less than 0")

    lines = []
    for i in range(total_number):
        log.debug("line content: %s,%s", i, random.random())
        lines.append([i, random.random()])

    return lines
