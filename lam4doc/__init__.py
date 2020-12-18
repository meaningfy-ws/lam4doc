#!/usr/bin/python3

# __init__.py
# Date:  17/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

import logging.config
from pathlib import Path

logging.config.fileConfig(Path(__file__).parents[1] / 'logging.conf')
