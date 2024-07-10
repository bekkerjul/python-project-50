from gendiff.scripts.gendiff import load_format, compare_keys, format_diff, generate_diff, define_format
import json, yaml

path1 = 'tests/fixtures/file1.json'
path2 = 'tests/fixtures/file2.json'
path3 = 'tests/fixtures/file3.yaml'
path4 = 'tests/fixtures/file4.yml'


def test_generate_diff_json():
    assert generate_diff(path1, path2) == open('tests/fixtures/result1.txt').read()

def test_generate_diff_yaml():
    assert generate_diff(path3, path4) == open('tests/fixtures/result2.txt').read()