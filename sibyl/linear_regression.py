import os
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from logger import log
from data_generator import rand


def calc_linear_fomula(json_data):
    log.debug("json_data: %s", json_data)
