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


def dfs_node(node, node_dict):
    """
    :param node:  BookmarkTitle类
    :param node_dict: 用于存放子文件夹和子书签的字典
    :return: 返回root节点的dict，用于转为markdown
    """
    node_name = node.getFullName()  # 名字
    singleton = Singleton.getInstance()
    for child in singleton.getChildren(node_name):  # 找儿子节点
        child_name = child.getFullName()
        child_url = child.getUrl()
        if not child_url:  # 非叶节点（文件夹）
            child_dict = OrderedDict()
            node_dict[child_name] = child_dict
            dfs_node(child, child_dict)
        else:  # 叶节点（书签）
            if 'url_content' not in node_dict:
                node_dict['url_content'] = ''
            node_dict['url_content'] = node_dict['url_content'] + '[' + child_name + ']' + '(' + child_url + ')\n'
            node_dict.move_to_end('url_content', last=False)    # 将url_content移到最前面，便于后续转为markdown
    return node_dict


def dfs_format(root, layer, markdown_str):
    """
    :param root: OrderedDict
    :param layer: 层数
    :param markdown_str: markdown的字符串表示
    :return: 当前层的markdown表示
    """
    for k, v in root.items():
        if k == 'url_content':
            markdown_str += str(v)
        elif type(v) == OrderedDict:
            markdown_str += '#'*layer + ' ' + str(k) + '\n'    # 标题栏
            markdown_str += dfs_format(v, layer+1, '')
    return markdown_str

