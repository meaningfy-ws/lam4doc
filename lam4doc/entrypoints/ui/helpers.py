#!/usr/bin/python3

# helpers.py
# Date:  06/01/2021
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

"""
Misfit methods
"""
from json import loads


def get_error_message_from_response(response):
    return f'Status: {loads(response).get("status")}. Title: {loads(response).get("title")}' \
           f' Detail: {loads(response).get("detail")}'
