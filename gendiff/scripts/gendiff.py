#!/usr/bin/env python3
import argparse
import json


def generate_diff(path1, path2):
    with open(path1) as file1, open(path2) as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)

    diff = {}

    keys1 = set(data1.keys())
    keys2 = set(data2.keys())

    all_keys = keys1 | keys2
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

    diff_str = '{\n'
    for key, value in diff.items():
        if 'unchanged' in value:
            diff_str += f'    {key}: {value["first_file"]}\n'
        else:
            if value['first_file'] is not None:
                diff_str += f'  - {key}: {value["first_file"]}\n'
            if value['second_file'] is not None:
                diff_str += f'  + {key}: {value["second_file"]}\n'
    diff_str += '}'

    return diff_str


def main():
    parser = argparse.ArgumentParser(prog='gendiff',
                                     description='Compares two'
                                                 'configuration files '
                                                 'and shows a difference')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format',
                        help='set format of output', default='default')

    args = parser.parse_args()

    print(f'gendiff {args.first_file} {args.second_file}')
    diff_result = generate_diff(args.first_file, args.second_file)
    print(diff_result)


if __name__ == '__main__':
    main()
