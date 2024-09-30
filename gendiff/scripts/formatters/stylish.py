def stringify_value(key, val, sign, indent):
    if isinstance(val, dict):
        items = []
        for subkey, subval in val.items():
            items.append(stringify_value(subkey, subval, ' ', indent + '    '))
        return f"{indent}  {sign} {key}: {{\n{''.join(items)}{indent}    }}\n"
    elif isinstance(val, list):
        items = [stringify_value("", item, ' ', indent + '    ') for item in val]
        return f"{indent}  {sign} {key}: [\n{''.join(items)}{indent}    ]\n"
    else:
        return f"{indent}  {sign} {key}: {val}\n"


# def stylish(diff, depth=0):
#     print(f"stylish{diff}")
#     diff_str = '{\n'
#     indent = '    ' * depth
#     for key, val in diff.items():
#         if val['type'] == 'removed':
#             diff_str += f'{stringify_value(key, val["value"], "-", indent)}'
#         elif val['type'] == 'added':
#             diff_str += f'{stringify_value(key, val["value"], "+", indent)}'
#         elif val['type'] == 'unchanged':
#             diff_str += f'{indent}    {key}: {val["value"]}\n'
#         elif val['type'] == 'nested':
#             diff_str += f'{indent}    {key}: {stylish(val["value"],depth + 1)}\n'.rstrip()
#         else:
#             diff_str += f'{stringify_value(key, val["value"][0], "-", indent)}'
#             diff_str += f'{stringify_value(key, val["value"][1], "+", indent)}'
#     diff_str += f'{indent}}}'
#     return diff_str

def stylish(diff, depth=0):
    print(f"stylish{diff}")
    lines = []
    lines.append('    ' * depth+'{')
    indent = '    ' * depth
    for key, val in diff.items():
        if val['type'] == 'removed':
            lines.append(f'{indent}- {key}: {val["value"]}')
        elif val['type'] == 'added':
            lines.append(f'{indent}+ {key}: {val["value"]}')
        elif val['type'] == 'unchanged':
            lines.append(f'{indent}  {key}: {val["value"]}')
        elif val['type'] == 'nested':
            lines.append(f'{indent}  {key}: {{\n{stylish(val["value"], depth+1)}\n{indent}}}')
        else:
            lines.append(f'{indent}- {key}: {val["value"][0]}')
            lines.append(f'{indent}+ {key}: {val["value"][1]}')
    # lines.append('')
    return '\n'.join(lines)
