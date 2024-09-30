import json


def format_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, str):
        return f"'{value}'"
    elif value is None:
        return 'null'
    else:
        return json.dumps(value)


def plain(diff, path=''):
    diff_str = []
    for key, value in diff.items():
        current_path = f"{path}{key}"
        if value['type'] == 'removed':
            diff_str.append(f"Property '{current_path}' was removed")
        elif value['type'] == 'added':
            diff_str.append(f"Property '{current_path}' was added with value: {format_value(value['value'])}")
        elif value['type'] == 'unchanged':
            continue
        elif value['type'] == 'nested':
            nested_diff = plain(value["value"], path=f'{current_path}.')
            diff_str.append(nested_diff)
        else:
            diff_str.append(f"Property '{current_path}' was updated. From {format_value(value['value'][0])} to {format_value(value['value'][1])}")
    return '\n'.join(diff_str)


"""


def plain(diff, path=''):
    diff_str = 'Property '
    for key, value in diff.items():
        path += key
        if value['type'] == 'removed':
            diff_str += f"'{path}' was removed\n"
        elif value['type'] == 'added':
            diff_str += f"'{path}' was added with value: '{value[value]}'\n"
        elif value['type'] == 'unchanged':
            continue
        elif value['type'] == 'nested':
            path += plain(value["value"], path=f'{key}.')
        else:
            diff_str += f"'{path}' was updated. From {value['value'][0]} to {value['value'][1]}\n"
    return '\n'.join(diff_str)
"""