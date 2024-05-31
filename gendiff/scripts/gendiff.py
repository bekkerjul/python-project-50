import json
import yaml

from gendiff.parser import make_parser


def load_format(path, format_method):
    with open(path) as file:
        data = format_method(file)
    return data


def find_keys_tree(tree, tree_keys=None):
    if tree_keys is None:
        tree_keys = set()
    for key in tree:
        if isinstance(tree[key], dict):
            find_keys_tree(tree[key], tree_keys)
        tree_keys.add(key)
    return tree_keys


def compare_keys(data1, data2):
    keys1 = find_keys_tree(data1)
    keys2 = find_keys_tree(data2)
    all_keys = keys1 | keys2
    return all_keys


def define_format(path):
    if 'json' in path:
        make_format = json.load
    elif 'yaml' or 'yml' in path:
        make_format = yaml.safe_load
    return make_format


def format_diff(diff, depth=1):
    diff_str = '{\n'
    for key, val in diff.items():
        if isinstance(val, dict):
            depth += 1
            format_diff(val, depth)

        if val and val.get('unchanged'):
            diff_str += f'{"    " * depth}{key}: {val["first_file"]}\n'
        else:
            if val['first_file'] is not None:
                diff_str += f'{"  " * depth}- {key}: {val["first_file"]}\n'
            if val['second_file'] is not None:
                diff_str += f'{"  " * depth}+ {key}: {val["second_file"]}\n'
            diff_str += '}'
    return diff_str


def generate_diff_tree(data1, data2):
    diff = {}
    all_keys = compare_keys(data1, data2)

    for key in sorted(all_keys):
        val1 = data1.get(key)
        val2 = data2.get(key)

        if isinstance(val1, dict) and isinstance(val2, dict):
            diff[key] = generate_diff_tree(val1, val2)
        elif isinstance(val1, dict):
            diff[key] = {'first_file': val1, 'second_file': None}
        elif isinstance(val2, dict):
            diff[key] = {'first_file': None, 'second_file': val2}
        elif val1 != val2:
            diff[key] = {'first_file': val1, 'second_file': val2}
        else:
            diff[key] = {'first_file': val1, 'second_file': val2, 'unchanged': True}

    return diff


def generate_diff(path1, path2):
    data1 = load_format(path1, define_format(path1))
    data2 = load_format(path2, define_format(path2))

    diff = generate_diff_tree(data1, data2)
    return format_diff(diff)


def main():
    make_parser(generate_diff)


if __name__ == '__main__':
    main()