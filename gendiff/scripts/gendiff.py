import json
import yaml


# from gendiff.parser import make_parser


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


def stringify_value(key, val, sign, indent):
    if isinstance(val, dict):
        key2 = list(val)[0]
        return (f'{indent}  {sign} {key}: {{\n{indent}        '
                f'{key2}: {val[key2]}\n{indent}    }}\n ')
    else:
        return f'{indent}  {sign} {key}: {val}\n'


def format_diff(diff, depth=0):
    diff_str = '{\n'
    indent = '    ' * depth
    for key, val in diff.items():
        if val['type'] == 'removed':
            diff_str += f'{stringify_value(key, val["value"], "-", indent)}'
        elif val['type'] == 'added':
            diff_str += f'{stringify_value(key, val["value"], "+", indent)}'
        elif val['type'] == 'unchanged':
            diff_str += f'{indent}    {key}: {val["value"]}\n'
        elif val['type'] == 'nested':
            diff_str += f'{indent}    {key}: {format_diff(val["value"], depth + 1)}\n'
        else:
            diff_str += f'{stringify_value(key, val["value"][0], "-", indent)}'
            diff_str += f'{stringify_value(key, val["value"][1], "+", indent)}'
    diff_str += f'{indent}}}'
    return diff_str


"""
   for key, val in diff.items():
     if isinstance(val, dict) and key != 'type':
         format_diff(val, depth+1)

     if val['type'] == 'added':
         diff_str += f'{indent}+ {key}: {val["value"]}\n'
     elif val['type'] == 'removed':
         diff_str += f'{indent}+ {key}: {val["value"]}\n'
     elif val['type'] == 'changed':
         diff_str += f'{indent}- {key}: {val["value"]}\n'
         diff_str += f'{indent}+ {key}: {val["value"]}\n'
     else:
         diff_str += f'{indent}  {key}: {val["value"]}\n'
 return diff_str




depth += 1
            diff_str += '{\n'
            format_diff(val['first_file'], depth, diff_str)
        if val['type'] == 'added':
            diff_str += f'{"  " * (depth - 2)}- {key}: {val["first_file"]}\n'
        elif val['type'] == 'removed':
            diff_str += f'{"  " * (depth - 2)}+ {key}: {val["second_file"]}\n'
        elif val['type'] == 'changed':
            diff_str += f'{"  " * (depth - 2)}- {key}: {val["first_file"]}\n'
            diff_str += f'{"  " * (depth - 2)}+ {key}: {val["second_file"]}\n'
        else:
            diff_str += f'{"  " * depth}{key}: {val["first_file"]}\n'
    return diff_str
"""


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


def generate_diff(path1, path2):
    data1 = load_format(path1, define_format(path1))
    data2 = load_format(path2, define_format(path2))

    diff = generate_diff_tree(data1, data2)
    return format_diff(diff)


"""
def main():
    make_parser(generate_diff)


if __name__ == '__main__':
    main()
"""
path1 = 'C:/Users/Юля/Documents/python-project-50/tests/fixtures/file3.yaml'
path2 = 'C:/Users/Юля/Documents/python-project-50/tests/fixtures/file4.yml'
data1 = load_format(path1, yaml.safe_load)
data2 = load_format(path2, yaml.safe_load)
# print(generate_diff(path1, path2))
diff = (generate_diff_tree(data1, data2))
print(format_diff(diff))
# print(diff)
