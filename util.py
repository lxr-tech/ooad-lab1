import re
import os
import json
from typing import List

from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester

# from Component import *


def markdown_to_dict(markdown_file):
    nester = CMarkASTNester()
    renderer = Renderer()
    f = open(markdown_file, 'r', encoding='UTF-8', errors='ignore')
    ast = CommonMark.DocParser().parse(f.read())
    f.close()
    nested = nester.nest(ast)
    rendered = renderer.stringify_dict(nested)
    rendered = json.loads(json.dumps(rendered))
    return rendered


def every(lst, fn=lambda x: x):
    return all(map(fn, lst))


def get_cur_root_and_name():
    path = os.getcwd().replace('\\', '/')
    name = path.split('/')[-1]
    root = '/'.join(path.split('/')[:-1])
    return name, root


def get_bmk_name_and_url(string: str):
    name = re.findall(r'\[.+?\]', string)[0].replace('[', '').replace(']', '')
    url = re.findall(r'\(.+?\)', string)[0].replace('[', '').replace(']', '')
    return name, url


# class Destroyer:
#
#     def __init__(self, createStrategy: CreateStrategy):
#         self.createStrategy = createStrategy
#
#     def destroy(self, item):
#         pass

