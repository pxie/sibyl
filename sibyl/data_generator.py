import random
from logger import log


def rand(total_number):
    log.info("generate random data from 0 - 1")
    if total_number < 0:
        return log.info("input total_number is less than 0")

    lines = []
    for i in range(total_number):
        num = 0.05 * i + random.random()
        log.debug("line content: %s,%s", i, num)
        lines.append([i, num])

    return {"values": lines}
