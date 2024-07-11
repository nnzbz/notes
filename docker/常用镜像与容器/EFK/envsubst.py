# -*- coding: utf-8 -*-
# 通过环境变量注入模板生成文件
# 参考https://www.cnblogs.com/leoninew/p/13516223.html
import argparse
import logging
import os
import sys
from typing import Dict, Iterable


class EnvironmentContext:
    _args: Dict[str, str]

    def __init__(self, env_ignore: bool):
        if env_ignore:
            self._args = {}
        else:
            self._args = os.environ.copy()

    def update(self, args: Dict[str, str]):
        self._args.update(args)

    def transform(self, input: str) -> str:
        for k, v in self._args.items():
            # ${key} = value
            k2 = '${' + k + '}'
            input = input.replace(k2, v, -1)
        return input


def _parse_env_args(lines: Iterable[str]) -> Dict[str, str]:
    dict = {}
    for line in lines:
        arr = line.split('=', 1)
        assert len(arr) == 2, 'Arg "{}" invalid'.format(line)
        dict[arr[0]] = arr[1]
    return dict


def _parse_env_file(env_file: str) -> Dict[str, str]:
    dict = {}
    with open(env_file) as f:
        for num, line in enumerate(f):
            if line and line.strip() != "" and not line.startswith('#'):
                arr = line.split('=', 1)
                assert len(arr) == 2, 'Arg "{}" invalid'.format(line)
                dict[arr[0]] = arr[1].strip().strip('"')
    return dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # 直接输入环境变量行内键值对字符串
    parser.add_argument('--env', dest='env', type=str, nargs='*', required=False)
    # 输入环境变量文件
    parser.add_argument('--env-file', dest='env_file', action='store', required=False)
    # 忽略外部环境变量
    parser.add_argument('--env-ignore', dest='env_ignore', help='ignore environment variables', action='store_true', required=False)
    # 输入模板文件
    parser.add_argument('-f', '--file', dest='file', action='store', required=False)
    # 输入模板字符串
    parser.add_argument('-i', '--input', dest='input', action='store', required=False)

    if len(sys.argv) <= 2:
        parser.print_help()
    else:
        argv = parser.parse_args()
        context = EnvironmentContext(argv.env_ignore)
        if argv.env_file:
            env_args = _parse_env_file(argv.env_file)
            context.update(env_args)
        if argv.env:
            env_args = _parse_env_args(argv.env)
            context.update(env_args)

        input = argv.input
        if argv.file:
            with open(argv.file) as f:
                input = f.read()
        output = context.transform(input)
        print(output)
