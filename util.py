import os
import sys
import csv
import json
from Component import *
from collections import OrderedDict
from typing import List


from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester


def get_input():
    args = [line for line in csv.reader([input(">>> ").replace('\'', '\"')],
                                        skipinitialspace=True, delimiter=' ')][0]
    return [arg.replace('\'', '').replace('\"', '') for arg in args]


def update_sys_argv(new_argv):
    sys.argv = [sys.argv[0]]
    sys.argv.extend(new_argv)


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

