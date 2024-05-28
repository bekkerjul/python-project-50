from gendiff.scripts.gendiff import generate_diff

def test_gendiff():
    path1 = 'tests/fixtures/file1.json'
    path2 = 'tests/fixtures/file2.json'

    assert generate_diff(path1, path2) == open('tests/fixtures/result1.txt').read()
