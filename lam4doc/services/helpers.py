#!/usr/bin/python3

# helpers.py
# Date:  23/12/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

import logging
from collections import namedtuple

from lam4doc.config import LAM_LOGGER

logger = logging.getLogger(LAM_LOGGER)

FileInfo = namedtuple('FileInfo', 'location file_name')
IndexInfo = namedtuple('IndexInfo', 'name, config_location')
