def formater_json(diff, depth=0):
    diff_str = '{\n'
    indent = '  ' * depth
    for key, val in diff.items():
        if val['type'] == 'removed':
            diff_str += f'{stringify_value(key, val["value"], "-", indent)}'
        elif val['type'] == 'added':
            diff_str += f'{stringify_value(key, val["value"], "+", indent)}'
        elif val['type'] == 'unchanged':
            diff_str += f'{indent}    {key}: {val["value"]}\n'
        elif val['type'] == 'nested':
            diff_str += f'{indent}    {key}: {stylish(val["value"], depth + 1)}\n'.rstrip()
        else:
            diff_str += f'{stringify_value(key, val["value"][0], "-", indent)}'
            diff_str += f'{stringify_value(key, val["value"][1], "+", indent)}'
        diff_str += f'{indent}}}'
        return diff_str

    {
        "common": {
            "setting1": "Value 1",
            "setting2": 200,
            "setting3": true,
            "setting6": {
                "key": "value",
                "doge": {
                    "wow": ""
                }
            }
        },
        "group1": {
            "baz": "bas",
            "foo": "bar",
            "nest": {
                "key": "value"
            }
        },
        "group2": {
            "abc": 12345,
            "deep": {
                "id": 45
            }
        }
    }