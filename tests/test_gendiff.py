from gendiff.scripts.gendiff import load_json, compare_keys, format_diff, generate_diff

path1 = 'tests/fixtures/file1.json'
path2 = 'tests/fixtures/file2.json'
path3 = 'tests/fixtures/file1.yaml'
data1 = {
        'host': 'hexlet.io',
        'timeout': 50,
        'proxy': '123.234.53.22',
        'follow': False
    }
data2 = {
  'timeout': 20,
  'verbose': True,
  'host': 'hexlet.io'
}
diff = {
    'follow': {'first_file': False, 'second_file': None},
    'host': {'first_file': 'hexlet.io', 'second_file': 'hexlet.io', 'unchanged': True},
    'proxy': {'first_file': '123.234.53.22', 'second_file': None},
    'timeout': {'first_file': 50, 'second_file': 20},
    'verbose': {'first_file': None, 'second_file': True}
}

def test_load_json():
    assert load_json(path1) == data1

def test_load_yaml():
    assert load_yaml(path3) == data1

def test_compare_keys():
    assert compare_keys(data1, data2) == {'host', 'timeout', 'proxy', 'follow', 'verbose'}


def test_format_diff():
    assert format_diff(diff) == open('tests/fixtures/result1.txt').read()


def test_generate_diff():
    assert generate_diff(path1, path2) == open('tests/fixtures/result1.txt').read()


