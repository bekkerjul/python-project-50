import json
import yaml
from gendiff.scripts.formatters.plain import plain
from gendiff.scripts.formatters.stylish import stylish
from gendiff.parser import make_parser


def load_format(path, format_method):
    with open(path) as file:
        data = format_method(file)
    return data


def find_keys_tree(tree):
    tree_keys = set()
    if isinstance(tree, dict):
        for key in tree:
            tree_keys.add(key)
        return tree_keys if tree_keys else None


def compare_keys(data1, data2):
    keys1 = find_keys_tree(data1)
    keys2 = find_keys_tree(data2)
    if keys1 and keys2:
        all_keys = keys1 | keys2
    elif keys1:
        all_keys = keys1
    else:
        all_keys = keys2
    return sorted(all_keys)


def define_format(path):
    if 'json' in path:
        make_format = json.load
    elif 'yaml' or 'yml' in path:
        make_format = yaml.safe_load
    return make_format


def generate_diff_tree(data1, data2):
    diff = {}
    all_keys = compare_keys(data1, data2)

    for key in all_keys:
        val1 = data1[key] if isinstance(data1, dict) and key in data1 else None
        val2 = data2[key] if isinstance(data2, dict) and key in data2 else None

        if key in data1 and key not in data2:
            diff[key] = {'type': 'removed', 'value': val1}
        elif key in data2 and key not in data1:
            diff[key] = {'type': 'added', 'value': val2}
        elif val1 == val2:
            diff[key] = {'type': 'unchanged', 'value': val1}
        elif isinstance(val1, dict) and isinstance(val2, dict):
            diff[key] = {'type': 'nested', 'value': generate_diff_tree(val1, val2)}
        else:
            diff[key] = {'type': 'changed', 'value': [val1, val2]}
    return diff


def generate_diff(path1, path2, formatter=stylish):
    data1 = load_format(path1, define_format(path1))
    data2 = load_format(path2, define_format(path2))
    print('to generate diff tree')
    diff = generate_diff_tree(data1, data2)
    print(diff)
    return stylish(diff)


def main():
    parser = make_parser(generate_diff)
    print(parser)
    args = parser.parse_args()
    formatters = {
        'stylish': stylish,
        'plain': plain
    }
    formatter = formatters.get(args.format, stylish)
    diff = generate_diff(args.first_file, args.second_file, formatter)
    print(diff)
    with open('result.txt', 'w', encoding='UTF8') as text:
        text.write(diff)


if __name__ == '__main__':
    main()
"""
path1 = 'C:/Users/Юля/Documents/python-project-50/tests/fixtures/fixtures_yaml/file3.yaml'
path2 = 'C:/Users/Юля/Documents/python-project-50/tests/fixtures/fixtures_yaml/file4.yml'
data1 = load_format(path1, yaml.safe_load)
data2 = load_format(path2, yaml.safe_load)
# print(generate_diff(path1, path2))
diff = (generate_diff_tree(data1, data2))
#print(format_diff(diff))
print(diff)
"""