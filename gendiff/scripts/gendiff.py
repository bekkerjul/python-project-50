#!/usr/bin/env python3
import json
import yaml

from gendiff.parser import make_parser


def load_format(path, format_method):
    with open(path) as file:
        data = format_method(file)
    return data


def compare_keys(data1, data2):
    keys1 = set(data1.keys())
    keys2 = set(data2.keys())
    all_keys = keys1 | keys2
    return all_keys


def format_diff(diff):
    diff_str = '{\n'
    for key, value in sorted(diff.items()):
        if value.get('unchanged'):
            diff_str += f'    {key}: {value["first_file"]}\n'
        else:
            if value['first_file'] is not None:
                diff_str += f'  - {key}: {value["first_file"]}\n'
            if value['second_file'] is not None:
                diff_str += f'  + {key}: {value["second_file"]}\n'
    diff_str += '}'
    return diff_str


def define_format(path):
    if 'json' in path:
        make_format = json.load
    elif 'yaml' or 'yml' in path:
        make_format = yaml.safe_load
    return make_format


def generate_diff(path1, path2):
    data1 = load_format(path1, define_format(path1))
    data2 = load_format(path2, define_format(path2))

    diff = {}
    all_keys = compare_keys(data1, data2)

    for key in sorted(all_keys):
        if key in data1 and key in data2:
            if data1[key] != data2[key]:
                diff[key] = {'first_file': data1[key],
                             'second_file': data2[key]}
            else:
                diff[key] = {'first_file': data1[key],
                             'second_file': data2[key], 'unchanged': True}
        elif key in data1:
            diff[key] = {'first_file': data1[key],
                         'second_file': None}
        else:
            diff[key] = {'first_file': None, 'second_file': data2[key]}

    return format_diff(diff)


def main():
    make_parser(generate_diff)


if __name__ == '__main__':
    main()
