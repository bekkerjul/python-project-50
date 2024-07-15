from gendiff.scripts.gendiff import generate_diff

path1 = 'tests/fixtures/file1.json'
path2 = 'tests/fixtures/file2.json'
path3 = 'tests/fixtures/file3.yaml'
path4 = 'tests/fixtures/file4.yml'


def test_generate_diff_json_stylish():
    assert generate_diff(path1, path2, stylish) == open('tests/fixtures/result1.txt').read()


def test_generate_diff_yaml_stylish():
    assert generate_diff(path3, path4, stylish) == open('tests/fixtures/result2.txt').read()


def test_generate_diff_json_plain():
    assert generate_diff(path1, path2, plain) == open('tests/fixtures/result3.txt').read()

